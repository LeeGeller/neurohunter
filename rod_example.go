package main

import (
	"fmt"
	"net/url"

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
		fmt.Println("Company", vacancyPage.MustElement("a[href*='/companies/']").MustText())
		conditionsTitle, err := vacancyPage.ElementR(
			"h2.content-section__title",
			"Условия",
		)

		if err != nil {
			fmt.Println("Не найден заголовок Условия:", err)
			continue
		}

		conditionsSection := conditionsTitle.MustParent().MustParent()

		workFormat, err := conditionsSection.Element(".chip-with-icon__text")

		if err != nil {
			fmt.Println("Не найден формат работы:", err)
			continue
		}

		fmt.Println("WorkFormat:", workFormat.MustText())

		//fmt.Println("WorkFormat:", vacancyPage.
		//	MustElement(`use[xlink\:href*="#format"]`).
		//	MustParent().
		//	MustParent().
		//	MustElement(".chip-with-icon__text").
		//	MustText())

	}
}
