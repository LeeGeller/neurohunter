package main

import (
	"log"
	"net/http"
	"neurohunter/handlers"
)

func main() {

	http.HandleFunc("/search", handlers.SearchHandler)

	log.Println("server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))

}
