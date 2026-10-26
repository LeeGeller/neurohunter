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
	seenVacancyUsers := make(map[string]struct{})

	for jobTitle, userIDs := range jobTitleGroups {
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
			vacancyID := strings.TrimSpace(vacancy.ID)

			if vacancyID == "" {
				log.Printf(
					"Skipping vacancy without ID: %q",
					vacancy.Title,
				)
				continue
			}

			// Проверяем вакансию по ограничениям пользователей,
			// связанным с текущим поисковым тайтлом.
			matchedUsers := make([]string, 0)

			for _, userID := range userIDs {
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
					matchedUsers = append(matchedUsers, userID)
				}
			}

			// Если вакансия не подошла ни одному пользователю,
			// не добавляем её в общий список.
			if len(matchedUsers) == 0 {
				continue
			}

			// Добавляем вакансию в общий список только один раз.
			if _, exists := seenVacancies[vacancyID]; !exists {
				allVacancies = append(allVacancies, vacancy)
				seenVacancies[vacancyID] = struct{}{}
			}

			// Формируем связи вакансии со всеми подходящими пользователями.
			for _, userID := range matchedUsers {
				userID = strings.TrimSpace(userID)
				if userID == "" {
					continue
				}

				associationKey := vacancyID + ":" + userID

				if _, exists := seenVacancyUsers[associationKey]; exists {
					continue
				}

				vacancyUser = append(
					vacancyUser,
					models.VacancyUser{
						VacancyID: vacancyID,
						UserID:    userID,
					},
				)

				seenVacancyUsers[associationKey] = struct{}{}
			}
		}
	}

	return allVacancies, vacancyUser, nil
}
