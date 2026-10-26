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
) ([]models.Vacancy, []models.VacancyUser, error) {
	// Получаем группы профессий из Python Analyzer.
	jobTitleGroups, err := analyzerClient.GetJobTitleGroups(ctx)
	if err != nil {
		return nil, nil, err
	}

	userFeatures, err := analyzerClient.GetUserFeatures(ctx)
	if err != nil {
		return nil, nil, err
	}

	allVacancies := make([]models.Vacancy, 0)
	seenVacancies := make(map[string]struct{})
	vacancyUser := make([]models.VacancyUser, 0)

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

			// Пропускаем дубликаты до фильтрации.
			if _, exists := seenVacancies[key]; exists {
				continue
			}

			// Проверяем вакансию по ограничениям пользователей,
			// связанным с текущим поисковым тайтлом.
			matchesAnyUser := false

			for _, userID := range userIDS {
				userFeature, exists := userFeatures[userID]
				if !exists {
					log.Printf(
						"User features not found for user ID %s",
						userID,
					)
					continue
				}

				if filtering.FilterVacanciesByUserFeatures(
					vacancy,
					userFeature,
				) {
					matchesAnyUser = true
					break
				}
			}

			// Если вакансия не подошла ни одному пользователю,
			// не добавляем её в общий список.
			if !matchesAnyUser {
				continue
			}

			// Добавляем вакансию после успешной фильтрации.
			allVacancies = append(allVacancies, vacancy)
			seenVacancies[key] = struct{}{}
		}
	}

	return allVacancies, vacancyUser, nil
}
