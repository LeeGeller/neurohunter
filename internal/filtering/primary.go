package filtering

import (
	"neurohunter/models"
)

func FilterVacanciesByUserFeatures(
	vacancy models.Vacancy,
	userFeature models.UserFeature,
) bool {
	hardConstraints := userFeature.HardConstraints

	if hardConstraints.Salary != nil &&
		*vacancy.SalaryFrom <= *hardConstraints.Salary {
		return false
	}

	return true
}
