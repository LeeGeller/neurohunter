package search

import "neurohunter/models"

func BuildVacancyUser(
	vacancyID string,
	userID string,
) models.VacancyUser {
	return models.VacancyUser{
		VacancyID: vacancyID,
		UserID:    userID,
	}
}
