package four

import (
	"strings"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

type Entry struct {
	number int
	marked bool
}

type Board struct {
	rows [][]*Entry
}

func NewBoard(input string) *Board {
	split := strings.Split(input, "\n")
	rows := [][]*Entry{}

	for _, line := range split {
		clean := util.Filter(strings.Split(line, " "), func(t string) bool { return t != "" })
		rows = append(rows, util.Map(util.Ints(clean), func(i int) *Entry { return &Entry{i, false} }))
	}

	return &Board{rows}
}

func (b *Board) MarkNumber(n int) {
	for _, v := range b.rows {
		for _, e := range v {
			if e.number == n {
				e.marked = true
			}
		}
	}
}

func (b *Board) Wins() bool {
	for _, row := range b.rows {
		if util.All(row, func(t *Entry) bool { return t.marked }) {
			return true
		}
	}

outer:
	for i := 0; i < len(b.rows[0]); i++ {
		for _, row := range b.rows {
			if !row[i].marked {
				continue outer
			}
		}

		return true
	}

	return false
}

func (b *Board) Numbers() []*Entry {
	return util.Chain(b.rows...)
}

func ParseInput(input string) ([]int, []*Board) {
	split := util.SectionedInput(input)

	randomNums := util.Ints(strings.Split(split[0], ","))
	boards := []*Board{}

	for _, board := range split[1:] {
		boards = append(boards, NewBoard(board))
	}

	return randomNums, boards
}

func Solve1(input string) int {
	nums, boards := ParseInput(input)
	for _, n := range nums {
		for _, b := range boards {
			b.MarkNumber(n)
			if b.Wins() {
				unmarked := util.Filter(b.Numbers(), func(e *Entry) bool { return !e.marked })
				return util.Sum(util.Map(unmarked, func(e *Entry) int { return e.number })) * n
			}
		}
	}
	return -1
}

func Solve2(input string) int {
	nums, boards := ParseInput(input)
	winningBoards := []int{}

	for _, n := range nums {
		for i, b := range boards {
			b.MarkNumber(n)
			if util.Contains(winningBoards, i) {
				continue
			}

			if b.Wins() {
				winningBoards = append(winningBoards, i)

				if len(winningBoards) == len(boards) {
					unmarked := util.Filter(b.Numbers(), func(e *Entry) bool { return !e.marked })
					return util.Sum(util.Map(unmarked, func(e *Entry) int { return e.number })) * n
				}

			}
		}
	}
	return -2
}
