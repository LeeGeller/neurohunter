package search

import (
	"context"
	"log"
	"strings"

	"neurohunter/internal/filtering"
	"neurohunter/internal/scraper/habr"
	"neurohunter/internal/users"
	"neurohunter/models"
)

func FetchVacanciesHabr(
	ctx context.Context,
	analyzerClient *users.Client,
) ([]models.Vacancy, error) {
	// Получаем группы профессий из Python Analyzer.
	jobTitleGroups, err := analyzerClient.GetJobTitleGroups(ctx)
	if err != nil {
		return nil, err
	}

	userFeatures, err := analyzerClient.GetUserFeatures(ctx)
	if err != nil {
		return nil, err
	}

	// Собираем вакансии по всем поисковым запросам.
	allVacancies := make([]models.Vacancy, 0)
	seenVacancies := make(map[string]struct{})

	for jobTitle, userIDS := range jobTitleGroups {
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

		for _, userID := range userIDS {
			userFeature, exists := userFeatures[userID]

			if !exists {
				log.Printf("User features not found for user ID %s", userID)
				continue
			}

			filteredVacancy := filtering.FilterVacanciesByUserFeatures(vacancies, userFeature)
		}
	}

	return allVacancies, nil
}
