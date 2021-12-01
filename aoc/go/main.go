package main

import (
	"fmt"
	"os"
	"strconv"
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

var allDays = func() (out []int) {
	for i := 1; i <= 25; i++ {
		out = append(out, i)
	}
	return
}()

func main() {
	args := os.Args

	toDo := []int{}

	if util.Contains(args, "all") {
		toDo = allDays
	} else if len(args) > 1 {
		// we got a list of args
		for _, v := range args[1:] {
			res, err := strconv.Atoi(v)
			if err != nil {
				continue
			}

			toDo = append(toDo, res)
		}
	} else {

		now := time.Now()
		day, month := now.Day(), time.Now().Month()
		if day <= 25 && month == time.December {
			toDo = append(toDo, day)
		} else {
			// do them all, yes this is a copy of above
			toDo = allDays
		}
	}

	for _, i := range toDo {
		if len(SOLUTIONS) >= i {
			s := SOLUTIONS[i-1]
			input := util.GetInput(i)
			t1, res1 := timeRun(s[0], input)
			t2, res2 := timeRun(s[1], input)

			fmt.Printf("Day %02d: Part 1: %s (%s)\n", i, res1, t1)
			fmt.Printf("Day %02d: Part 2: %s (%s)\n", i, res2, t2)
		} else {
			fmt.Printf("Day %02d: Part 1: Not found (0ns)\n", i)
			fmt.Printf("Day %02d: Part 2: Not found (0ns)\n", i)
		}
		fmt.Println()
	}
}
