package eleven

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

func tupleEq(a, b [2]int) bool {
	return a[0] == b[0] && a[1] == b[1]
}

func Step(grid [][]int) [][]int {
	flashed := [][2]int{}

	var flash func(row, oct int)

	flash = func(row, oct int) {
		if util.ContainsFunc(flashed, [2]int{row, oct}, tupleEq) {
			return
		}

		flashed = append(flashed, [2]int{row, oct})

		for _, d := range util.CARDINAL_DIAG {
			newRow, newOct := row+d[0], oct+d[1]

			if !util.SafeDir(grid, newRow, newOct) {
				continue
			}

			grid[newRow][newOct]++
			if grid[newRow][newOct] > 9 {
				flash(newRow, newOct)
			}
		}
	}
	for row := range grid {
		for oct := range grid[row] {
			grid[row][oct]++
		}
	}

	for row := range grid {
		for oct := range grid[row] {
			if grid[row][oct] > 9 {
				flash(row, oct)
			}
		}
	}

	for _, pair := range flashed {
		grid[pair[0]][pair[1]] = 0
	}

	return grid
}

func parseGrid(input string) [][]int {
	return util.Map(strings.Split(input, "\n"), func(t string) []int { return util.Ints(strings.Split(t, "")) })
}

func Solve1(input string) int {
	// 	input = `5483143223
	// 2745854711
	// 5264556173
	// 6141336146
	// 6357385478
	// 4167524645
	// 2176841721
	// 6882881134
	// 4846848554
	// 5283751526`

	grid := parseGrid(input)

	printGrid := func(g [][]int) {
		for _, line := range g {
			fmt.Println(strings.Join(util.Map(line, strconv.Itoa), ""))
		}
	}
	_ = printGrid

	flashCount := 0

	for i := 1; i < 101; i++ {
		grid = Step(grid)

		for _, r := range grid {
			for _, c := range r {
				if c == 0 {
					flashCount++
				}
			}
		}
	}

	return flashCount
}

func Solve2(input string) int {
	grid := parseGrid(input)

	printGrid := func(g [][]int) {
		for _, line := range g {
			fmt.Println(strings.Join(util.Map(line, strconv.Itoa), ""))
		}
	}
	_ = printGrid

	gridSize := len(grid) * len(grid[0])

	i := 0

	for {
		i++
		grid = Step(grid)
		fc := 0
		for _, r := range grid {
			for _, c := range r {
				if c == 0 {
					fc++
				}
			}
		}

		if fc == gridSize {
			break
		}
	}

	return i
}
