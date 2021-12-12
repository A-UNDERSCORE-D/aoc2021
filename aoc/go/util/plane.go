package util

var (
	NORTH = [2]int{1, 0}
	EAST  = [2]int{0, 1}
	SOUTH = [2]int{-1, 0}
	WEST  = [2]int{0, -1}

	NORTH_EAST = [2]int{1, 1}
	NORTH_WEST = [2]int{1, -1}
	SOUTH_EAST = [2]int{-1, 1}
	SOUTH_WEST = [2]int{-1, -1}

	CARDINAL = [...][2]int{
		NORTH, EAST, SOUTH, WEST,
	}

	CARDINAL_DIAG = [...][2]int{
		NORTH, EAST, SOUTH, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST,
	}
)

func SafeDir[T any](grid [][]T, row, col int) bool {
	if row >= len(grid) || row < 0 {
		return false
	}

	if col >= len(grid[0]) || col < 0 {
		return false
	}

	return true
}
