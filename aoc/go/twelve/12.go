package twelve

import (
	"strings"

	"github.com/A-UNDERSCORE-D/aoc2021/aoc/go/util"
)

type Node struct {
	Name       string
	Small      bool
	Neighbours []*Node
}

func (n *Node) String() string {
	return n.Name
}

func NewNode(name string) *Node {
	return &Node{
		Name:  name,
		Small: strings.ToLower(name) == name,
	}
}

func (*Node) Eq(self, other *Node) bool {
	return self.Name == other.Name
}

func RecurseBFS(currentNode *Node, currentPath []*Node, partOne bool) [][]*Node {
	path := append([]*Node(nil), currentPath...)
	path = append(path, currentNode)

	out := make([][]*Node, 0, len(currentNode.Neighbours))

nodeLoop:
	for _, n := range currentNode.Neighbours {
		if n.Name == "end" {
			copy := append([]*Node(nil), path...)
			copy = append(copy, n)
			out = append(out, copy)

			continue
		}

		if n.Name == "start" {
			continue
		}

		if n.Small {
			nInCurrentPath := util.ContainsFunc(path, n, n.Eq)
			if partOne && nInCurrentPath {
				continue
			}

			if !partOne && nInCurrentPath {
				// have we visited any node twice?
				m := map[*Node]int{}

				for _, v := range path {
					if !v.Small {
						continue
					}

					m[v]++
					if m[v] == 2 {
						partOne = true
						continue nodeLoop
					}
				}
			}
		}

		newPath := append([]*Node(nil), path...)
		res := RecurseBFS(n, newPath, partOne)

		out = append(out, res...)

	}

	return out
}

func newGraph(input string) map[string]*Node {
	split := util.Map(strings.Split(input, "\n"), func(t string) []string { return strings.Split(t, "-") })
	graph := map[string]*Node{}

	for _, pair := range split {
		start_name, end_name := pair[0], pair[1]

		var start, end *Node

		if res, exists := graph[start_name]; exists {
			start = res
		} else {
			start = NewNode(start_name)
		}

		if res, exists := graph[end_name]; exists {
			end = res
		} else {
			end = NewNode(end_name)
		}

		if !util.ContainsFunc(start.Neighbours, end, start.Eq) {
			start.Neighbours = append(start.Neighbours, end)
		}

		if !util.ContainsFunc(end.Neighbours, start, start.Eq) {
			end.Neighbours = append(end.Neighbours, start)
		}

		graph[start_name] = start
		graph[end_name] = end

	}

	return graph
}

func Solve1(input string) int {
	g := newGraph(input)
	paths := RecurseBFS(g["start"], []*Node{}, true)

	return len(paths)
}

func Solve2(input string) int {
	g := newGraph(input)
	paths := RecurseBFS(g["start"], []*Node{}, false)

	return len(paths)
}
