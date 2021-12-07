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

func All[T any](slice []T, pred func(T) bool) bool {
	for _, v := range slice {
		if !pred(v) {
			return false
		}
	}

	return true
}

func Any[T any](slice []T, pred func(T) bool) bool {
	for _, v := range slice {
		if pred(v) {
			return true
		}
	}
	return false
}

func Map[T any, U any](slice []T, pred func(T) U) []U {
	out := make([]U, 0, len(slice))
	for _, v := range slice {
		out = append(out, pred(v))
	}

	return out
}

func Filter[T any](slice []T, pred func(T) bool) []T {
	out := make([]T, 0, len(slice))
	for _, v := range slice {
		if pred(v) {
			out = append(out, v)
		}
	}

	return out
}

func Chain[T any](slices ...[]T) []T {
	l := 0
	for _, v := range slices {
		l += len(v)
	}

	out := make([]T, 0, l)

	for _, s := range slices {
		out = append(out, s...)
	}

	return out
}

func Min[T Number](slice []T) T {
	if len(slice) == 0 {
		panic("attempt to min slice of length 0")
	}
	min := slice[0]

	for _, v := range slice[1:] {
		if v < min {
			min = v
		}
	}

	return min
}

func Max[T Number](slice []T) T {
	if len(slice) == 0 {
		panic("attempt to min slice of length 0")
	}
	max := slice[0]

	for _, v := range slice[1:] {
		if v > max {
			max = v
		}
	}

	return max
}
