package two

import (
	"strings"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

type Sub struct {
	horiz int
	depth int
	aim   int
}

func (s *Sub) move(instruction string, count int, part2 bool) {
	switch instruction {
	case "forward":
		s.horiz += count

		if part2 {
			s.depth += s.aim * count
		}

	case "up":
		if !part2 {
			s.depth -= count
		} else {
			s.aim -= count
		}

	case "down":
		if !part2 {
			s.depth += count
		} else {
			s.aim += count
		}
	default:
		panic("Unknown")
	}
}

func Solve1(input string) int {
	lines := strings.Split(input, "\n")
	sub := Sub{}

	for _, l := range lines {
		split := strings.Split(l, " ")
		instruction, count := split[0], util.MustInt(split[1])
		sub.move(instruction, count, false)
	}

	return sub.horiz * sub.depth
}

func Solve2(input string) int {
	lines := strings.Split(input, "\n")
	sub := Sub{}

	for _, l := range lines {
		split := strings.Split(l, " ")
		instruction, count := split[0], util.MustInt(split[1])
		sub.move(instruction, count, true)
	}

	return sub.horiz * sub.depth
}
