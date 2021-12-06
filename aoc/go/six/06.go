package six

import (
	"strings"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

func runFish(input [9]uint64, days uint64) uint64 {
	for i := uint64(0); i < days; i++ {
		new := [9]uint64{}
		for i := 0; i < 9; i++ {
			switch i {
			case 0:
				new[6] += input[0]
				new[8] += input[0]
			default:
				new[i-1] += input[i]
			}
		}

		input = new
	}

	var out uint64
	for _, v := range input {
		out += v
	}

	return out
}

func Solve1(input string) int {
	ints := util.Ints(strings.Split(input, ","))

	realInput := [9]uint64{}
	for _, v := range ints {
		realInput[v] += 1
	}

	return int(runFish(realInput, 80))
}

func Solve2(input string) int {
	ints := util.Ints(strings.Split(input, ","))

	realInput := [9]uint64{}
	for _, v := range ints {
		realInput[v] += 1
	}

	return int(runFish(realInput, 256))
}
