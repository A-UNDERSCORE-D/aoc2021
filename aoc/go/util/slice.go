package util

import (
	"constraints"
	"reflect"
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

type Comparable interface {
	constraints.Complex | constraints.Ordered
}

func Index[T Comparable](slice []T, value T) int {
	for i, v := range slice {
		if v == value {
			return i
		}
	}

	return -1
}

func IndexFunc[T any](slice []T, value T, eq func(T, T) bool) int {
	for i, v := range slice {
		if eq(v, value) {
			return i
		}
	}

	return -1
}

func Contains[T Comparable](slice []T, value T) bool {
	return Index(slice, value) != -1
}

func ContainsFunc[T any](slice []T, value T, eq func(T, T) bool) bool {
	return IndexFunc(slice, value, eq) != -1
}

func ReflectCompare[T any](a, b T) bool {
	return reflect.DeepEqual(a, b)
}
