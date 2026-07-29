package model

import "time"

type Vacancy struct {
	ID           string
	Title        string
	Company      string
	WorkLocation *string
	WorkFormat   *string
	URL          string
	Description  string
	SalaryFrom   *int
	SalaryTo     *int
	Currency     *string
	VacancyDate  time.Time
}
