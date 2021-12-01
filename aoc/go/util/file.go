package util

import (
	"fmt"
	"os"
)

func GetInput(day int) string {
	res, err := os.ReadFile(fmt.Sprintf("../input/%02d.input", day))
	if err != nil {
		panic(err)
	}

	return string(res)
}
