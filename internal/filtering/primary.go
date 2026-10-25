package filtering

import (
	"neurohunter/models"
)

func FilterVacanciesByUserFeatures(
	vacancies []models.Vacancy,
	userFeatures []models.UserFeature,
	userIDs []string,
) []models.Vacancy {

	// TODO: фильтрация по зарплате, локации и формату работы.
	return vacancies
}
