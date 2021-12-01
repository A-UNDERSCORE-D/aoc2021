package one

import (
	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

func Solve1(input string) int {
	count := 0
	ints := util.Ints(util.Lines(input))

	for _, v := range util.Window(ints, 2) {
		if len(v) != 2 {
			continue
		}
		if v[1] > v[0] {
			count++
		}
	}

	return count
}

func Solve2(input string) int {
	count := 0
	ints := util.Ints(util.Lines(input))
	windows := util.Window(ints, 3)
	zipped := util.Zip(windows, windows[1:])

	for _, v := range zipped {
		if len(v[0]) != 3 || len(v[1]) != 3 {
			continue
		}

		if util.Sum(v[1]) > util.Sum(v[0]) {
			count++
		}
	}

	return count
}
