use std::fmt::Debug;

use itertools::Itertools;

fn parse(input: &String) -> Grid {
    Grid {
        0: input
            .lines()
            .map(|x| x.split("").flat_map(str::parse).collect_vec())
            .collect_vec(),
    }
}

struct Grid(Vec<Vec<u8>>);
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Point {
    x: usize,
    y: usize,
}

impl Point {
    fn new(x: usize, y: usize) -> Point {
        Point { x, y }
    }
}

impl Debug for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("({},{})", self.x, self.y))
    }
}
impl Grid {
    fn safe_positions(&self, start: Point) -> Vec<Point> {
        let mut out = Vec::new();
        let (xbound, ybound) = self.bounds();
        if start.x + 1 < xbound {
            out.push(Point::new(start.x + 1, start.y))
        }

        if start.x != 0 {
            out.push(Point::new(start.x - 1, start.y))
        }

        if start.y + 1 < ybound {
            out.push(Point::new(start.x, start.y + 1))
        }

        if start.y != 0 {
            out.push(Point::new(start.x, start.y - 1))
        }

        out
    }

    fn low_points(&self) -> Vec<Point> {
        let (xbound, ybound) = self.bounds();
        let mut low_points = Vec::new();

        for x in 0..xbound {
            for y in 0..ybound {
                let p = Point::new(x, y);
                let current = self.at(p);
                if self.safe_positions(p).iter().all(|x| self.at(*x) > current) {
                    low_points.push(p);
                }
            }
        }

        low_points
    }

    fn basins(&self) -> Vec<Vec<Point>> {
        let mut low_points = self.low_points();
        let mut basins = Vec::new();

        while low_points.len() > 0 {
            let basin = self.bfs_from(low_points.pop().unwrap());
            low_points = low_points
                .into_iter()
                .filter(|x| !basin.contains(x))
                .collect_vec();

            basins.push(basin)
        }

        basins
    }

    fn bfs_from(&self, start: Point) -> Vec<Point> {
        let mut checked = Vec::new();
        let mut to_check = Vec::new();
        to_check.push(start);

        while to_check.len() > 0 {
            let next = to_check.pop().unwrap();
            checked.push(next);

            to_check.extend(
                self.safe_positions(next)
                    .iter()
                    .filter(|&&x| self.at(x) != 9 && !checked.contains(&x)),
            );
        }

        checked
    }

    fn bounds(&self) -> (usize, usize) {
        (self.0[0].len(), self.0.len())
    }

    fn at(&self, p: Point) -> u8 {
        self.0[p.y][p.x]
    }

    #[allow(dead_code)]
    fn string(&self, highlight: &Vec<Point>) -> String {
        let (xb, yb) = self.bounds();
        let mut out = String::new();
        for x in 0..xb {
            for y in 0..yb {
                let p = Point::new(x, y);
                if highlight.contains(&p) {
                    out.push_str(format!("\x1b[1m{}\x1b[m", self.at(p)).as_str())
                } else {
                    out.push(' ');
                    // out.push_str(format!("{}", self.at(p)).as_str())
                }
            }
            out.push('\n');
        }

        out
    }
}

pub fn part_1(input: &String) -> u32 {
    let input = parse(input);

    let low_points = input.low_points();
    low_points.iter().map(|&x| input.at(x) as u32 + 1).sum()
}

pub fn part_2(input: &String) -> usize {
    let input = parse(input);
    let basins = input.basins();

    let mut largest = Vec::new();

    for b in basins {
        let mut b = b.clone();
        b.sort();
        b.dedup();

        if largest.len() != 3 {
            largest.push(b.len());
            largest.sort();
        } else {
            let mut to_set = 4;
            for (i, &other) in largest.iter().enumerate() {
                if b.len() > other {
                    to_set = i;
                    break;
                }
            }

            if to_set < 4 {
                largest[to_set] = b.len()
            }
        }
    }

    largest[0] * largest[1] * largest[2]
}
