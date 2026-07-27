package model

type Vacancy struct {
	ID           int
	Title        string
	Company      string
	WorkLocation string
	WorkFormat   string
	URL          string
	Description  string
	SalaryFrom   int
	SalaryTo     int
	Currency     string
	Skills       string
}
