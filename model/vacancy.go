package model

type Vacancy struct {
	ID          int
	Title       string
	Company     string
	Location    string
	Description string
	URL         string
	SalaryFrom  int
	SalaryTo    int
	City        string
}
