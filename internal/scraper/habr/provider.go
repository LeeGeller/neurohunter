package habr

import (
	"io"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"

	"neurohunter/internal/utils"
	"neurohunter/model"

	"github.com/PuerkitoBio/goquery"
)

const baseURL = "https://career.habr.com"

var client = &http.Client{
	Timeout: 20 * time.Second,
}

func fetchHTML(link string) (io.ReadCloser, error) {
	req, err := http.NewRequest(http.MethodGet, link, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set(
		"User-Agent",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/138 Safari/537.36",
	)

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != http.StatusOK {
		resp.Body.Close()
		return nil, &url.Error{
			Op:  "GET",
			URL: link,
			Err: io.ErrUnexpectedEOF,
		}
	}

	return resp.Body, nil
}

func FetchHabrVacancies(query string) ([]model.Vacancy, error) {
	searchURL := baseURL + "/vacancies?q=" + url.QueryEscape(query)

	body, err := fetchHTML(searchURL)
	if err != nil {
		return nil, err
	}
	defer body.Close()

	doc, err := goquery.NewDocumentFromReader(body)
	if err != nil {
		return nil, err
	}

	var vacancyURLs []string

	doc.Find(".vacancy-card__title-link").Each(func(_ int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if !ok {
			return
		}

		vacancyURLs = append(vacancyURLs, baseURL+href)
	})

	var (
		wg       sync.WaitGroup
		sem      = make(chan struct{}, 25)
		resultCh = make(chan model.Vacancy)
	)

	for _, link := range vacancyURLs {
		wg.Add(1)

		go func(link string) {
			defer wg.Done()

			sem <- struct{}{}
			defer func() { <-sem }()

			vacancy, err := parseVacancy(link)
			if err != nil {
				return
			}

			resultCh <- vacancy
		}(link)
	}

	go func() {
		wg.Wait()
		close(resultCh)
	}()

	var vacancies []model.Vacancy

	for vacancy := range resultCh {
		vacancies = append(vacancies, vacancy)
	}

	return vacancies, nil
}

func parseVacancy(link string) (model.Vacancy, error) {
	body, err := fetchHTML(link)
	if err != nil {
		return model.Vacancy{}, err
	}
	defer body.Close()

	doc, err := goquery.NewDocumentFromReader(body)
	if err != nil {
		return model.Vacancy{}, err
	}

	vacancyID := utils.ParseVacancyID(link)

	title := strings.TrimSpace(doc.Find(".page-title__title").First().Text())

	company := strings.TrimSpace(doc.Find(".company_name").First().Text())

	description := strings.TrimSpace(
		doc.Find(".vacancy-description__text").First().Text(),
	)

	var (
		workLocation *string
		workFormat   *string
		salaryFrom   *int
		salaryTo     *int
		currency     *string
		vacancyDate  time.Time
	)

	// --------------------
	// Conditions
	// --------------------

	doc.Find("h2.content-section__title").EachWithBreak(func(_ int, s *goquery.Selection) bool {

		if strings.TrimSpace(s.Text()) != "Условия" {
			return true
		}

		meta := s.Parent().Parent().Find(".vacancy-meta")

		if meta.Length() == 0 {
			return false
		}

		// Cities
		var cities []string

		meta.Find(".basic-chip").Each(func(_ int, chip *goquery.Selection) {

			if chip.Find(".svg-icon--icon-placemark").Length() == 0 {
				return
			}

			city := strings.TrimSpace(
				chip.Find(".chip-with-icon__text").Text(),
			)

			if city != "" {
				cities = append(cities, city)
			}
		})

		if len(cities) > 0 {
			location := strings.Join(cities, ", ")
			workLocation = &location
		}

		// Work format
		meta.Find(".basic-chip").Each(func(_ int, chip *goquery.Selection) {

			if workFormat != nil {
				return
			}

			if chip.Find(".svg-icon--icon-format").Length() == 0 {
				return
			}

			format := strings.TrimSpace(
				chip.Find(".chip-with-icon__text").Text(),
			)

			if format != "" {
				workFormat = &format
			}
		})

		return false
	})

	// --------------------
	// Salary
	// --------------------

	salaryInfo := strings.TrimSpace(
		doc.Find(".basic-salary").First().Text(),
	)

	if salaryInfo != "" {
		salaryFrom, salaryTo = utils.Parse(salaryInfo)

		cur := utils.ParseCurrency(salaryInfo)
		if cur != "" {
			currency = &cur
		}
	}

	// --------------------
	// Published date
	// --------------------

	if datetime, ok := doc.Find("time.basic-date").Attr("datetime"); ok {
		if parsed, err := time.Parse(time.RFC3339, datetime); err == nil {
			vacancyDate = parsed
		}
	}

	return model.Vacancy{
		ID:           vacancyID,
		Title:        title,
		Company:      company,
		Description:  description,
		WorkLocation: workLocation,
		WorkFormat:   workFormat,
		SalaryFrom:   salaryFrom,
		SalaryTo:     salaryTo,
		Currency:     currency,
		URL:          link,
		VacancyDate:  vacancyDate,
	}, nil
}
