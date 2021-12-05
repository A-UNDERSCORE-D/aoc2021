use std::{collections::HashMap, fmt::Debug, panic};

#[allow(dead_code)]
const TEST_INPUT: &str = r"0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";

fn nice_range(a: i32, b: i32) -> Vec<i32> {
    if a > b {
        return ((b + 1)..a).rev().collect();
    }

    return ((a + 1)..b).collect();
}

#[derive(Clone, Copy, Hash, PartialEq, Eq)]
struct Point {
    x: i32,
    y: i32,
}

impl Debug for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("Point(x:{}, y:{})", self.x, self.y))
    }
}

impl Point {
    fn new(x: i32, y: i32) -> Point {
        Point { x, y }
    }
}

struct LineSegment {
    start: Point,
    end: Point,
}

impl LineSegment {
    fn is_horiz(&self) -> bool {
        self.start.x == self.end.x
    }

    fn is_vert(&self) -> bool {
        self.start.y == self.end.y
    }

    fn is_45(&self) -> bool {
        self.slope().abs() == 1.0
    }

    fn slope(&self) -> f64 {
        let dy: f64 = (self.end.y - self.start.y).into();
        let dx: f64 = (self.end.x - self.start.x).into();
        return dy / dx;
    }

    fn points(&self) -> Vec<Point> {
        if self.is_horiz() {
            let mut out = nice_range(self.start.y, self.end.y)
                .iter()
                .map(|y| Point {
                    x: self.start.x,
                    y: *y,
                })
                .collect::<Vec<_>>();

            out.insert(0, self.start);
            out.push(self.end);
            return out;
        } else if self.is_vert() {
            let mut out = nice_range(self.start.x, self.end.x)
                .iter()
                .map(|x| Point {
                    y: self.start.y,
                    x: *x,
                })
                .collect::<Vec<_>>();

            out.insert(0, self.start);
            out.push(self.end);
            return out;
        } else if self.is_45() {
            let xs = nice_range(self.start.x, self.end.x);
            let ys = nice_range(self.start.y, self.end.y);
            let mut between: Vec<_> = xs.iter().zip(ys).map(|(x, y)| Point { x: *x, y }).collect();
            between.insert(0, self.start);
            between.push(self.end);
            return between;
        }

        panic!("???");
    }

    fn new(line: &str) -> LineSegment {
        let split: Vec<(i32, i32)> = line
            .split(" -> ")
            .map(|x| x.split(","))
            .map(|x| {
                let l: Vec<&str> = x.collect();
                (l[0].parse().unwrap(), l[1].parse().unwrap())
            })
            .collect();

        return LineSegment {
            start: Point::new(split[0].0, split[0].1),
            end: Point::new(split[1].0, split[1].1),
        };
    }
}

impl Debug for LineSegment {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("LS(S:{:?}, E:{:?})", self.start, self.end))
    }
}

pub fn part_1(input: &String) -> usize {
    let lines = input
        .lines()
        .map(LineSegment::new)
        .filter(|l| l.is_horiz() || l.is_vert())
        .collect::<Vec<_>>();
    let points = lines.iter().flat_map(|l| l.points());

    let mut overlaps: HashMap<Point, usize> = HashMap::new();

    for p in points {
        if overlaps.contains_key(&p) {
            *overlaps.get_mut(&p).unwrap() += 1
        } else {
            overlaps.insert(p, 1);
        }
    }

    overlaps.values().filter(|x| **x > 1).count()
}

pub fn part_2(input: &String) -> usize {
    let lines = input.lines().map(LineSegment::new).collect::<Vec<_>>();
    let points = lines.iter().flat_map(|l| l.points());

    let mut overlaps: HashMap<Point, usize> = HashMap::new();

    for p in points {
        if overlaps.contains_key(&p) {
            *overlaps.get_mut(&p).unwrap() += 1
        } else {
            overlaps.insert(p, 1);
        }
    }

    overlaps.values().filter(|x| **x > 1).count()
}
