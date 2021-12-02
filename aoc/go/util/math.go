package util

import "strconv"

func MustInt(s string) int {
	res, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}

	return res
}
