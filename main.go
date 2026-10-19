package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"neurohunter/config"
	"neurohunter/database"
	"neurohunter/handlers"
	"neurohunter/internal/users"
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

	// Для тестирования получаем данные из Analyzer и выводим их в лог.
	analyzerClient, err := users.NewClient(
		cfg.UserFeaturesURL,
		cfg.JobTitleGroupsURL,
	)
	if err != nil {
		log.Printf("Analyzer client initialization failed: %v", err)
	} else {
		ctx, cancel := context.WithTimeout(
			context.Background(),
			30*time.Second,
		)

		features, featuresErr := analyzerClient.GetUserFeatures(ctx)
		if featuresErr != nil {
			log.Printf("Failed to get user features: %v", featuresErr)
		} else {
			log.Printf("Received %d user profiles from Analyzer", len(features))
			printJSON("USER FEATURES", features)
		}

		groups, groupsErr := analyzerClient.GetJobTitleGroups(ctx)
		if groupsErr != nil {
			log.Printf("Failed to get job title groups: %v", groupsErr)
		} else {
			log.Printf("Received %d job title groups from Analyzer", len(groups))
			printJSON("JOB TITLE GROUPS", groups)
		}

		cancel()
	}

	http.HandleFunc("/search", handlers.SearchHandler(mongoDB))

	log.Printf("Go service listening on port %s", cfg.AppPort)
	log.Fatal(http.ListenAndServe(":"+cfg.AppPort, nil))
}

// Временно используем для проверки ответов Analyzer
func printJSON(label string, value any) {
	data, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		log.Printf("Failed to encode %s: %v", label, err)
		return
	}

	log.Printf("\n=== %s ===\n%s", label, data)
}
