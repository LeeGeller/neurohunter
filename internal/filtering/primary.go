package filtering

import (
	"neurohunter/models"
)

func FilterVacanciesByUserFeatures(
	vacancy []models.Vacancy,
	userFeature []models.UserFeature,
) []models.Vacancy {

	if vacancy.Salary < userFeature.Salary {
		return nil
	}

}
