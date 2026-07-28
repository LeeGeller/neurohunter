package main

import (
	"log"
	"net/http"
	"neurohunter/config"
	"neurohunter/handlers"
)

func main() {

	config, err := config.LoadConfig()

	if err != nil {
		log.Fatal(err)
	}

	http.HandleFunc("/search", handlers.SearchHandler)

	log.Printf("server started on :%s", config.AppPort)
	log.Fatal(http.ListenAndServe(":"+config.AppPort, nil))

}
