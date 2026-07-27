package main

import (
	"fmt"
	"net/url"
	"neurohunter/internal/habr/salary"
	"strings"

	"github.com/go-rod/rod"
)

func main() {
	browser := rod.New().MustConnect()

	defer browser.MustClose()

	searchURL := "https://career.habr.com/vacancies?q=" + url.QueryEscape("golang")

	page := browser.MustPage(searchURL).MustWaitLoad()

	fmt.Println("Страница поиска открыта")

	vacancies := page.MustElements(".vacancy-card")

	fmt.Println("Найдено вакансий:", len(vacancies))

	//var result []model.Vacancy

	for _, vacancy := range vacancies {

		link := vacancy.MustElement(".vacancy-card__title-link")

		href := link.MustAttribute("href")

		fmt.Println("URL:", *href)

		//result = append(result, model.Vacancy{
		//	Title:       vacancyPage.MustElement("page-title__title").MustText(),
		//	Company:     vacancyPage.MustElement(".company_name").MustText(),
		//	WorkFormat:  vacancyPage.MustElement(`use[xlink\:href*="#format"]`).MustText(),
		//	Description: vacancyPage.MustElement(".vacancy__description").MustText(),
		//	URL:         "https://career.habr.com" + *href,
		//	SalaryInfo:  vacancyPage.MustElement(".basic-salary").MustText(),
		//	Skills:      vacancyPage.MustElement(".content-section content-section--appearance-chips-meta").MustText(),
		//})

		vacancyPage := browser.
			MustPage("https://career.habr.com" + *href).
			MustWaitLoad()

		fmt.Println("Страница вакансии открыта")
		fmt.Println("Title:", vacancyPage.MustElement(".page-title__title").MustText())
		fmt.Println("Company", vacancyPage.MustElement(".company_name").MustText())
		conditionsTitle, err := vacancyPage.ElementR(
			"h2.content-section__title",
			"Условия",
		)

		if err != nil {
			fmt.Println("Не найден заголовок Условия:", err)
			continue
		}

		conditionsSection := conditionsTitle.MustParent().MustParent()

		vacancyMeta, err := conditionsSection.Element(".vacancy-meta")

		if err != nil {
			fmt.Println("Не найден vacancy-meta:", err)
			continue
		}

		placeChips := vacancyMeta.MustElements(
			`.basic-chip:has(.svg-icon--icon-placemark)`,
		)
		var cities []string

		if placeChips == nil {
			fmt.Println("Город не указан")
		} else {
			for _, placeChip := range placeChips {
				workPlace := placeChip.MustElement(".chip-with-icon__text").MustText()

				cities = append(cities, strings.TrimSpace(workPlace))
			}
		}
		fmt.Println("Города:", cities)

		workFormatChip, err := vacancyMeta.Element(
			`.basic-chip:has(.svg-icon--icon-format)`,
		)

		if err != nil {
			fmt.Println("Формат работы не указан")
			continue
		} else {
			workFormat := workFormatChip.MustElement(
				".chip-with-icon__text",
			).MustText()

			fmt.Println("Формат работы:", workFormat)
		}

		description := vacancyPage.MustElement(".vacancy-description__text").MustText()

		fmt.Println("Описание:", description)

		salarySection, err := vacancyPage.Element(".vacancy-header__salary")

		if err != nil {
			fmt.Println("Зарплата не указана")
			continue
		}

		salaryElement, err := salarySection.Element(".basic-salary")

		if err != nil {
			fmt.Println("Зарплата не указана")
			continue
		}

		salaryInfo := salaryElement.MustText()

		salaryFrom, salaryTo := salary.Parse(salaryInfo)

		fmt.Println("Зарплата от:", salaryFrom)
		fmt.Println("Зарплата до:", salaryTo)
		fmt.Println("Валюта", salary.ParseCurrency(salaryInfo))

	}
}
