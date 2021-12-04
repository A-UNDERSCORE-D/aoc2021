use crate::aoc_util;
use std::fmt::Debug;
struct Board {
    rows: Vec<Vec<(u8, bool)>>,
}

impl Debug for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut out = String::new();

        for row in &self.rows {
            for (n, v) in row {
                out.push_str(
                    format!(
                        "{:<3}",
                        format!("{x}{n}{x}", n = n, x = if *v { "|" } else { "" })
                    )
                    .as_str(),
                );
            }
            out.push('\n');
        }

        f.write_str(out.as_str())
    }
}

impl Board {
    fn mark_number(&mut self, num: u8) {
        for row in self.rows.iter_mut() {
            for col in row {
                if col.0 == num {
                    col.1 = true
                }
            }
        }
    }

    fn wins(&self) -> bool {
        for row in &self.rows {
            if row.iter().all(|(_, m)| *m) {
                return true;
            }
        }

        for c_idx in 0..self.rows[0].len() {
            let mut ok = false;
            for r in &self.rows {
                if r[c_idx].1 {
                    ok = true
                } else {
                    ok = false;
                    break;
                }
            }

            if ok {
                return true;
            }
        }

        false
    }

    fn sum(&self) -> i32 {
        let mut out: i32 = 0;
        for (n, b) in self.rows.iter().flatten() {
            if !b {
                let n: i32 = (*n).into();
                out += n;
            }
        }

        out
    }

    fn new(raw: &String) -> Board {
        let mut rows: Vec<Vec<(u8, bool)>> = Vec::new();
        for line in raw.lines() {
            rows.push(
                line.split_whitespace()
                    .flat_map(str::parse)
                    .map(|x| (x, false))
                    .collect(),
            )
        }

        Board { rows }
    }
}

pub fn part_1(input: &String) -> i32 {
    let data = aoc_util::to_sectioned_string_vec(input);
    let (random_numbers, data) = data.split_first().expect("???");
    let random_numbers: Vec<i32> = random_numbers
        .split(",")
        .flat_map(str::parse::<i32>)
        .collect();

    let mut boards: Vec<Board> = data.iter().map(Board::new).collect();

    for n in random_numbers {
        for b in &mut boards {
            b.mark_number(n.try_into().unwrap());
            if b.wins() {
                return b.sum() * n;
            }
        }
    }

    0
}

pub fn part_2(input: &String) -> i32 {
    let data = aoc_util::to_sectioned_string_vec(input);
    let (random_numbers, data) = data.split_first().expect("???");
    let random_numbers: Vec<i32> = random_numbers
        .split(",")
        .flat_map(str::parse::<i32>)
        .collect();

    let mut boards: Vec<Board> = data.iter().map(Board::new).collect();
    let mut winning_boards: Vec<usize> = Vec::new();

    for n in random_numbers {
        let board_len = boards.len();
        for (i, b) in boards.iter_mut().enumerate() {
            b.mark_number(n.try_into().unwrap());
            if winning_boards.contains(&i) {
                continue;
            }

            if b.wins() {
                winning_boards.push(i);
                if winning_boards.len() == board_len {
                    return b.sum() * n;
                }
            }
        }
    }

    0
}
