package main

import (
	"context"
	"log"
	"net/http"
	"neurohunter/config"
	"neurohunter/database"
	"neurohunter/handlers"
)

func main() {

	config, err := config.LoadConfig()

	if err != nil {
		log.Fatal(err)
	}

	mongoDB, err := database.ConnectMongoDB(config.MONGO_URI)

	if err != nil {
		log.Fatal(err)
	}

	defer mongoDB.Disconnect(context.Background())

	http.HandleFunc("/search", handlers.SearchHandler(mongoDB))

	log.Fatal(http.ListenAndServe(":"+config.AppPort, nil))

	if err != nil {
		log.Fatal(err)
	}

}
