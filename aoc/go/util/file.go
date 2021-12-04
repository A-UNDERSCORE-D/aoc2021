package util

import (
	"fmt"
	"os"
	"strings"
)

func GetInput(day int) string {
	res, err := os.ReadFile(fmt.Sprintf("../input/%02d.input", day))
	if err != nil {
		panic(err)
	}

	return string(res)
}

func SectionedInput(input string) []string {
	return strings.Split(input, "\n\n")
}
