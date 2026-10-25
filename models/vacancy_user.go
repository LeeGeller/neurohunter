package models

type VacancyUser struct {
	VacancyID string `bson:"vacancy_id" json:"vacancy_id"`
	UserID    string `bson:"user_id" json:"user_id"`
}
