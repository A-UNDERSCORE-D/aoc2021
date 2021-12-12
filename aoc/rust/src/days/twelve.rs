use std::{collections::HashMap, fmt::Debug};

use itertools::Itertools;

type Graph<'a> = HashMap<&'a str, Node<'a>>;

struct Node<'a> {
    name: &'a str,
    small: bool,
    others: Vec<&'a str>,
}

impl Debug for Node<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("{} -> {}", self.name, self.others.join(",")))
    }
}

impl PartialEq for Node<'_> {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name
    }
}

fn construct_graph(input: &String) -> Graph {
    let mut g: Graph = HashMap::new();
    for pair in input.lines().map(|x| x.split("-").collect_tuple().unwrap()) {
        let (start, end) = pair;

        if let None = g.get(start) {
            g.insert(
                start,
                Node {
                    name: start,
                    small: start.to_lowercase() == start,
                    others: Vec::new(),
                },
            );
        }

        if let None = g.get(end) {
            g.insert(
                end,
                Node {
                    name: end,
                    small: end.to_lowercase() == end,
                    others: Vec::new(),
                },
            );
        }

        g.get_mut(start).unwrap().others.push(end);
        g.get_mut(end).unwrap().others.push(start);
    }

    g
}

fn recurse_bfs<'a>(
    current: &'a Node,
    graph: &'a Graph,
    source_path: &Vec<&'a Node<'_>>,
    part_1: bool,
) -> Vec<Vec<&'a Node<'a>>> {
    let mut part_1 = part_1;
    let mut current_path = source_path.clone();
    current_path.push(current);
    let mut out = Vec::new();

    for &name in &current.others {
        let node = &graph[name];
        if node.name == "start" {
            continue;
        }

        if node.name == "end" {
            let mut this_path = current_path.clone();
            this_path.push(node);

            out.push(this_path);
            continue;
        }
        if node.small {
            if part_1 && current_path.contains(&node) {
                continue;
            }

            let twos = current_path
                .iter()
                .filter(|x| x.small)
                .map(|&x| current_path.iter().filter(|&&o| x == o).count())
                .collect_vec();
            if !part_1 && current_path.contains(&node) && twos.iter().any(|&x| x > 1) {
                part_1 = true;
                continue;
            }
        }

        out.append(&mut recurse_bfs(
            &graph[name],
            graph,
            &current_path.clone(),
            part_1,
        ))
    }

    out
}

pub fn part_1(input: &String) -> usize {
    let g = construct_graph(input);
    let paths = recurse_bfs(&g["start"], &g, &vec![], true);

    paths.len()
}

pub fn part_2(input: &String) -> usize {
    let g = construct_graph(input);
    let paths = recurse_bfs(&g["start"], &g, &vec![], false);

    paths.len()
}
