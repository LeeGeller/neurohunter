package habr

import (
	"net/url"
	"strings"
	"sync"
	"time"

	"neurohunter/internal/habr/salary"
	"neurohunter/model"

	"github.com/go-rod/rod"
)

func FetchHabrVacancies(query string) ([]model.Vacancy, error) {
	browser := rod.New().MustConnect()

	defer browser.MustClose()

	searchURL := "https://career.habr.com/vacancies?q=" + url.QueryEscape(query)

	page := browser.
		MustPage(searchURL).
		MustWaitLoad()

	defer page.MustClose()

	// --------------------
	// Collect vacancy links
	// --------------------

	vacancyElements := page.MustElements(".vacancy-card")

	var vacancyURLs []string

	for _, vacancy := range vacancyElements {
		link, err := vacancy.Element(".vacancy-card__title-link")
		if err != nil {
			continue
		}

		href := link.MustAttribute("href")
		if href == nil {
			continue
		}

		vacancyURLs = append(
			vacancyURLs,
			"https://career.habr.com"+*href,
		)
	}

	// --------------------
	// Preparing for concurrent scraping
	// --------------------

	var wg sync.WaitGroup

	//Max 25 goroutines
	sem := make(chan struct{}, 25)

	resultChan := make(chan model.Vacancy)

	// --------------------
	// Start scraping
	// --------------------

	for _, vacancyURL := range vacancyURLs {
		wg.Add(1)

		go func(vacancyURL string) {
			defer wg.Done()

			// Получаем слот
			sem <- struct{}{}

			// Освобождаем слот
			defer func() {
				<-sem
			}()

			vacancy, err := parseVacancy(
				browser,
				vacancyURL,
			)

			if err != nil {
				return
			}

			resultChan <- vacancy

		}(vacancyURL)
	}

	// --------------------
	// Close channel after all goroutines finish
	// --------------------

	go func() {
		wg.Wait()
		close(resultChan)
	}()

	// --------------------
	// Collect results
	// --------------------

	var result []model.Vacancy

	for vacancy := range resultChan {
		result = append(result, vacancy)
	}

	return result, nil
}

func parseVacancy(
	browser *rod.Browser,
	href string,
) (model.Vacancy, error) {
	vacancyPage := browser.
		MustPage(href).
		MustWaitLoad()

	defer vacancyPage.MustClose()

	// --------------------
	// Base info
	// --------------------

	title := vacancyPage.
		MustElement(".page-title__title").
		MustText()

	company := vacancyPage.
		MustElement(".company_name").
		MustText()

	description := vacancyPage.
		MustElement(".vacancy-description__text").
		MustText()

	// --------------------
	// Conditions
	// --------------------

	var workLocation *string
	var workFormat *string

	conditionsTitle, err := vacancyPage.ElementR(
		"h2.content-section__title",
		"Условия",
	)

	if err == nil {
		conditionsSection := conditionsTitle.
			MustParent().
			MustParent()

		vacancyMeta, err := conditionsSection.Element(".vacancy-meta")

		if err == nil {

			// Cities
			placeChips := vacancyMeta.MustElements(
				`.basic-chip:has(.svg-icon--icon-placemark)`,
			)

			if len(placeChips) > 0 {
				var cities []string

				for _, placeChip := range placeChips {
					workPlace := placeChip.
						MustElement(".chip-with-icon__text").
						MustText()

					workPlace = strings.TrimSpace(workPlace)

					if workPlace != "" {
						cities = append(cities, workPlace)
					}
				}

				if len(cities) > 0 {
					location := strings.Join(cities, ", ")
					workLocation = &location
				}
			}

			// Work format
			workFormatChip, err := vacancyMeta.Element(
				`.basic-chip:has(.svg-icon--icon-format)`,
			)

			if err == nil {
				format := strings.TrimSpace(
					workFormatChip.
						MustElement(".chip-with-icon__text").
						MustText(),
				)

				if format != "" {
					workFormat = &format
				}
			}

		}
	}

	// --------------------
	// Salary
	// --------------------

	var salaryFrom *int
	var salaryTo *int
	var currency *string

	salaryElement, err := vacancyPage.
		Timeout(2 * time.Second).
		Element(".basic-salary")

	if err == nil {
		salaryInfo := salaryElement.MustText()

		salaryFrom, salaryTo = salary.Parse(salaryInfo)

		cur := salary.ParseCurrency(salaryInfo)

		if cur != "" {
			currency = &cur
		}
	}

	// --------------------
	// Date published
	// --------------------

	var vacancyDate time.Time

	dateElement, err := vacancyPage.Element("time.basic-date")

	if err == nil {
		datetime := dateElement.MustAttribute("datetime")

		if datetime != nil {
			publishedAt, err := time.Parse(
				time.RFC3339,
				*datetime,
			)

			if err == nil {
				vacancyDate = publishedAt
			}
		}
	}
	// --------------------
	// Return vacancy
	// --------------------

	return model.Vacancy{
		Title:        title,
		Company:      company,
		WorkLocation: workLocation,
		WorkFormat:   workFormat,
		URL:          href,
		Description:  description,
		SalaryFrom:   salaryFrom,
		SalaryTo:     salaryTo,
		Currency:     currency,
		VacancyDate:  vacancyDate,
	}, nil
}
