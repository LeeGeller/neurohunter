package filtering

import "neurohunter/models"

func FilterVacanciesByUserFeatures(
	vacancy models.Vacancy,
	userFeature models.UserFeature,
) bool {
	hardConstraints := userFeature.HardConstraints

	// Фильтрация по минимальной зарплате.
	if !checkSalary(vacancy, hardConstraints.Salary) {
		return false
	}

	// Фильтрация по формату работы.
	if !checkWorkFormat(vacancy, hardConstraints.WorkFormatConstraints) {
		return false
	}

	return true
}

func checkSalary(vacancy models.Vacancy, minSalary *int) bool {
	if minSalary == nil {
		return true
	}

	// Если зарплата не указана, нельзя подтвердить соответствие ограничению.
	if vacancy.SalaryFrom == nil {
		return false
	}

	return *vacancy.SalaryFrom >= *minSalary
}

func checkWorkFormat(
	vacancy models.Vacancy,
	constraints *models.WorkFormatConstraints,
) bool {
	// Ограничения по формату не заданы.
	if constraints == nil {
		return true
	}

	// Неизвестный формат пропускаем: отсутствие информации
	// ещё не означает, что вакансия не подходит.
	if vacancy.WorkFormat == nil {
		return true
	}

	switch *vacancy.WorkFormat {
	case "remote":
		return constraints.Remote == nil || *constraints.Remote

	case "office":
		return constraints.Office == nil || *constraints.Office

	case "hybrid":
		return constraints.Hybrid == nil || *constraints.Hybrid

	default:
		// Неизвестное значение формата не считаем несовместимым.
		return true
	}
}
