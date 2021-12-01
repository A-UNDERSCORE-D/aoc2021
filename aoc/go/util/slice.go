package util

import (
	"constraints"
	"strconv"
	"strings"
)

func Ints(slice []string) []int {
	out := make([]int, len(slice))
	for i, s := range slice {
		res, err := strconv.Atoi(s)
		if err != nil {
			panic(err)
		}

		out[i] = res
	}

	return out
}

func Lines(s string) []string { return strings.Split(s, "\n") }

func Window[T any](slice []T, n int) [][]T {
	out := [][]T{}

	for i := 0; i < len(slice); i++ {
		if i+n < len(slice) {
			out = append(out, slice[i:i+n])
		} else {
			out = append(out, slice[i:])
		}
	}

	return out
}

func Sum[T constraints.Integer](nums []T) T {
	var out T
	for _, v := range nums {
		out += v
	}

	return out
}

func Zip[T any](a, b []T) [][]T {
	longest := len(a)
	if len(b) > longest {
		longest = len(b)
	}

	var out [][]T

	for i := 0; i < longest; i++ {
		toSet := make([]T, 2)
		if i < len(a) {
			toSet[0] = a[i]
		}
		if i < len(b) {
			toSet[1] = b[i]
		}

		out = append(out, toSet)
	}

	return out
}
