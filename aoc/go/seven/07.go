package seven

import (
	"strings"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

func fuelCost(start, end int, exp bool) int {
	steps := util.Abs(start - end)

	if !exp {
		return steps
	}

	return steps * (steps + 1) / 2
}

func Solve1(input string) int {
	positions := util.Ints(strings.Split(input, ","))

	max := util.Max(positions)
	min := util.Min(positions)

	best_fuel := -1

	for i := min; i <= max; i++ {
		total := 0
		for _, p := range positions {
			total += fuelCost(p, i, false)
		}

		if total < best_fuel || best_fuel == -1 {
			best_fuel = total
		}
	}

	return best_fuel
}

func Solve2(input string) int {
	positions := util.Ints(strings.Split(input, ","))

	max := util.Max(positions)
	min := util.Min(positions)

	best_fuel := -1

	for i := min; i <= max; i++ {
		total := 0
		for _, p := range positions {
			total += fuelCost(p, i, true)
		}

		if total < best_fuel || best_fuel == -1 {
			best_fuel = total
		}
	}

	return best_fuel
}
