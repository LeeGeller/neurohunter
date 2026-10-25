package search

import (
	"context"
	"log"
	"strings"

	"neurohunter/internal/scraper/habr"
	"neurohunter/internal/users"
	"neurohunter/models"
)

func FetchVacancies(
	ctx context.Context,
	analyzerClient *users.Client,
) ([]models.Vacancy, error) {
	// Получаем группы профессий из Python Analyzer.
	jobTitleGroups, err := analyzerClient.GetJobTitleGroups(ctx)
	if err != nil {
		return nil, err
	}

	// Собираем вакансии по всем поисковым запросам.
	allVacancies := make([]models.Vacancy, 0)
	seenVacancies := make(map[string]struct{})

	for jobTitle := range jobTitleGroups {
		log.Printf("Searching vacancies for %q", jobTitle)

		vacancies, err := habr.FetchHabrVacancies(jobTitle)
		if err != nil {
			log.Printf(
				"Failed to fetch vacancies for %q: %v",
				jobTitle,
				err,
			)
			continue
		}

		for _, vacancy := range vacancies {
			key := strings.TrimSpace(vacancy.ID)

			if key == "" {
				log.Printf(
					"Skipping vacancy without ID: %q",
					vacancy.Title,
				)
				continue
			}

			// Пропускаем уже найденные вакансии.
			if _, exists := seenVacancies[key]; exists {
				continue
			}

			seenVacancies[key] = struct{}{}
			allVacancies = append(allVacancies, vacancy)
		}
	}

	log.Printf("Collected %d unique vacancies", len(allVacancies))

	return allVacancies, nil
}
