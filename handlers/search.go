package handlers

import (
	"encoding/json"
	"net/http"
	"neurohunter/internal/habr"
)

func SearchHandler(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query().Get("query")
	if query == "" {
		http.Error(w, "Query parameter is required", http.StatusBadRequest)
		return
	}

	vacancies, err := habr.FetchHabrVacancies(query)
	if err != nil {
		http.Error(w, "Failed to fetch vacancies", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(vacancies)
}
