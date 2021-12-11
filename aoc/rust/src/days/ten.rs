use std::collections::HashMap;

use itertools::Itertools;

const OPEN: &str = "([{<";
const CLOSE: &str = ")]}>";

fn validate(input: &str) -> (bool, Vec<char>) {
    let mut stack: Vec<char> = Vec::new();

    for (i, c) in input.chars().enumerate() {
        match c {
            '(' | '[' | '{' | '<' => stack.push(c),
            ')' | ']' | '}' | '>' => {
                let last = stack.pop().unwrap();
                let close_idx = CLOSE.find(c).unwrap();
                let opener = OPEN.chars().nth(close_idx).unwrap();
                if opener != last {
                    return (false, vec![c]);
                }
            }
            _ => panic!("??? {}:{}{}", input, i, c),
        }
    }

    (true, stack)
}

pub fn part_1(input: &String) -> usize {
    let points = HashMap::from([(')', 3), (']', 57), ('}', 1197), ('>', 25137)]);

    input
        .lines()
        .flat_map(|l| {
            let (valid, result) = validate(l);
            if valid {
                None
            } else {
                Some(points[&result[0]])
            }
        })
        .sum()
}

pub fn part_2(input: &String) -> usize {
    let points = HashMap::from([(')', 1), (']', 2), ('}', 3), ('>', 4)]);

    let results = input
        .lines()
        .flat_map(|l| {
            let (valid, res) = validate(l);
            if !valid {
                return None;
            }

            let to_fix = res
                .iter()
                .rev()
                .map(|x| CLOSE.chars().nth(OPEN.find(*x).unwrap()).unwrap())
                .collect_vec();

            // println!("{} {:?}", l, to_fix);

            Some(to_fix.iter().fold(0, |total, c| (total * 5) + points[c]))
        })
        .sorted()
        .collect_vec();

    results[results.len() / 2]
}
