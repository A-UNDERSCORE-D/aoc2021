package util

import (
	"constraints"
	"strconv"
)

func MustInt(s string) int {
	res, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}

	return res
}

type Number interface {
	constraints.Integer | constraints.Float
}

func Abs[T Number](a T) T {
	if a > 0 {
		return a
	}

	return -a
}
