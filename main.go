package main

import (
	"context"
	"log"
	"net/http"

	"neurohunter/config"
	"neurohunter/database"
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

	analyzerClient, err := users.NewClient(
		cfg.UserFeaturesURL,
		cfg.JobTitleGroupsURL,
	)
	if err != nil {
		log.Fatal(err)
	}

	log.Fatal(http.ListenAndServe(":"+cfg.AppPort, nil))
}
