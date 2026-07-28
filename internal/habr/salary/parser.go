package salary

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
