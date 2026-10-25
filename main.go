package main

import (
	"context"
	"log"

	"neurohunter/config"
	"neurohunter/internal/users"
	"neurohunter/search"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	analyzerClient, err := users.NewClient(
		cfg.UserFeaturesURL,
		cfg.JobTitleGroupsURL,
	)
	if err != nil {
		log.Fatal(err)
	}

	// Собираем вакансии по всем job_titles.
	vacancies, err := search.FetchVacanciesHabr(
		context.Background(),
		analyzerClient,
	)
	if err != nil {
		log.Printf("Failed to fetch vacancies: %v", err)
		return
	}

}
