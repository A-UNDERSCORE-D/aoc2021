use crate::aoc_util;

struct Sub {
    horiz: i64,
    depth: i64,
    aim: i64,
}

impl Sub {
    fn r#move(&mut self, instruction: &str, count: i64, part_1: bool) {
        match (instruction, count) {
            ("forward", x) => {
                self.horiz += x;
                if !part_1 {
                    self.depth += self.aim * x;
                }
            }

            ("up", x) => {
                if part_1 {
                    self.depth -= x;
                } else {
                    self.aim -= x;
                }
            }

            ("down", x) => {
                if part_1 {
                    self.depth += x
                } else {
                    self.aim += x
                }
            }
            (a, b) => println!("Unexpected: {} {}", a, b),
        }
    }
}

pub fn part_1(input: &String) -> i64 {
    let mut sub = Sub {
        aim: 0,
        depth: 0,
        horiz: 0,
    };
    for line in aoc_util::to_string_vec(input) {
        let mut split = line.split(" ");
        sub.r#move(
            split.next().unwrap(),
            split.next().unwrap().parse().unwrap(),
            true,
        )
    }

    sub.horiz * sub.depth
}

pub fn part_2(input: &String) -> i64 {
    let mut sub = Sub {
        aim: 0,
        depth: 0,
        horiz: 0,
    };
    for line in aoc_util::to_string_vec(input) {
        let mut split = line.split(" ");
        sub.r#move(
            split.next().unwrap(),
            split.next().unwrap().parse().unwrap(),
            false,
        )
    }

    sub.horiz * sub.depth
}
