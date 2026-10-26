package main

import (
	"context"
	"log"

	"neurohunter/config"
	"neurohunter/database"
	"neurohunter/internal/users"
	"neurohunter/search"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	mongoDB, err := database.ConnectMongoDB(cfg.MONGO_URI)

	if err != nil {
		log.Fatal(err)
	}

	defer mongoDB.Disconnect(context.Background())

	analyzerClient, err := users.NewClient(
		cfg.UserFeaturesURL,
		cfg.JobTitleGroupsURL,
	)
	if err != nil {
		log.Fatal(err)
	}

	// Собираем вакансии по всем job_titles.
	vacancies, vacancyUser, err := search.FetchVacanciesHabr(
		context.Background(),
		analyzerClient,
	)
	if err != nil {
		log.Printf("Failed to fetch vacancies: %v", err)
		return
	}

	// Сохраняем вакансии в MongoDB.
	if err := mongoDB.SaveVacancy(vacancies); err != nil {
		log.Printf("Failed to save vacancies: %v", err)
		return
	}
}
