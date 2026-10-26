package utils

import (
	"regexp"
	"strconv"
	"strings"
)

func Parse(text string) (from *int, to *int) {
	re := regexp.MustCompile(`(\d[\d\s]*)`)
	matches := re.FindAllString(text, -1)

	if len(matches) == 0 {
		return nil, nil
	}

	from = ParseNumberFromString(matches[0])

	if len(matches) > 1 {
		to = ParseNumberFromString(matches[1])
	}

	return from, to
}

func ParseNumberFromString(s string) *int {
	value := strings.ReplaceAll(s, " ", "")

	number, err := strconv.Atoi(value)

	if err != nil {
		return nil
	}

	return &number
}

func ParseCurrency(text string) string {
	reCode := regexp.MustCompile(`[A-Z]{3}`)
	code := reCode.FindString(text)

	if code != "" {
		return code
	}

	reSymbol := regexp.MustCompile(`[₽$€£]`)
	symbol := reSymbol.FindString(text)

	return symbol
}

func ParseVacancyID(href string) string {
	// Recieve href like https://career.habr.com/vacancy/123
	// Return 123
	parts := strings.Split(strings.TrimRight(href, "/"), "/")
	return parts[len(parts)-1]
}

// NormalizeWorkFormat converts a source work format into a stable value.
func NormalizeWorkFormat(raw string) *string {
	format := strings.ToLower(strings.TrimSpace(raw))
	format = strings.ReplaceAll(format, "ё", "е")

	var normalized string

	switch {
	case strings.Contains(format, "удал"),
		strings.Contains(format, "дистанц"),
		strings.Contains(format, "remote"):
		normalized = "remote"

	case strings.Contains(format, "офис"),
		strings.Contains(format, "office"):
		normalized = "office"

	case strings.Contains(format, "гибрид"),
		strings.Contains(format, "hybrid"):
		normalized = "hybrid"

	default:
		return nil
	}

	return &normalized
}
