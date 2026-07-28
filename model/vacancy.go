package model

import "time"

type Vacancy struct {
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
