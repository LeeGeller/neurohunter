package habr

import (
	"net/http"
	"net/url"

	"neurohunter/model"

	"github.com/PuerkitoBio/goquery"
)

func FetchHabrVacancies(query string) ([]model.Vacancy, error) {
	searchURL := "https://career.habr.com/vacancies?q=" + url.QueryEscape(query)

	resp, err := http.Get(searchURL)

	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)

	if err != nil {
		return nil, err
	}

	var result []model.Vacancy

	doc.Find(".vacancy-card__inner").Each(func(i int, s *goquery.Selection) {
		title := s.Find(".vacancy-card__title").Text()
		company := s.Find(".vacancy-card__company").Text()
		location := s.Find(".vacancy-card__meta-item--location").Text()
		description := s.Find(".vacancy-card__meta").Text()
		href, _ := s.Find(".vacancy-card__title-link").Attr("href")
		salary_info := s.Find(".vacancy-card__salary").Text()
		skills := s.Find(".vacancy-card__skills").Text()

		result = append(result, model.Vacancy{
			Title:       title,
			Company:     company,
			Location:    location,
			Description: description,
			URL:         href,
			SalaryInfo:  salary_info,
			SalaryFrom:  0,
			SalaryTo:    0,
			City:        location,
			Skills:      skills,
		})

	})
	return result, nil
}
