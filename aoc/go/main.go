package main

import (
	"fmt"
	"time"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/one"
	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

func makeString[T any](f func(string) T) func(string) string {
	return func(s string) string {
		return fmt.Sprint(f(s))
	}
}

var SOLUTIONS = [][2]func(string) string{
	{makeString(one.Solve1), makeString(one.Solve2)},
}

func timeRun(f func(string) string, s string) (time.Duration, string) {
	start := time.Now()
	res := f(s)
	return time.Since(start), res
}

func main() {
	for i, s := range SOLUTIONS {
		// continue
		input := util.GetInput(i + 1)
		t1, res1 := timeRun(s[0], input)
		t2, res2 := timeRun(s[1], input)

		fmt.Printf("Day %02d: Part 1: %s (%s)\n", i+1, res1, t1)
		fmt.Printf("Day %02d: Part 1: %s (%s)\n", i+1, res2, t2)
	}
}
