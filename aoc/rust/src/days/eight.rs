use std::{
    collections::{HashMap, HashSet},
    vec,
};

use itertools::Itertools;

struct Digit {
    number: u8,
    raw_mapping: [bool; 7],
}

impl Digit {
    fn mapped_str_mapping(&self, mapping: &Vec<&char>) -> String {
        let mut out = String::new();

        for (i, &c) in mapping.iter().enumerate() {
            if self.raw_mapping[i] {
                out.push(*c)
            }
        }

        out
    }
}

#[rustfmt::skip]
const DIGITS: [Digit; 10] = [
    Digit {number: 0, raw_mapping: [true, true, true, false, true, true, true]},        // 0
    Digit {number: 1, raw_mapping: [false, false, true, false, false, true, false]},    // 1
    Digit {number: 2, raw_mapping: [true, false, true, true, true, false, true]},       // 2
    Digit {number: 3, raw_mapping: [true, false, true, true, false, true, true]},       // 3
    Digit {number: 4, raw_mapping: [false, true, true, true, false, true, false]},      // 4
    Digit {number: 5, raw_mapping: [true, true, false, true, false, true, true]},       // 5
    Digit {number: 6, raw_mapping: [true, true, false, true, true, true, true]},        // 6
    Digit {number: 7, raw_mapping: [true, false, true, false, false, true, false]},     // 7
    Digit {number: 8, raw_mapping: [true, true, true, true, true, true, true]},         // 8
    Digit {number: 9, raw_mapping: [true, true, true, true, false, true, true]},        // 9
];

fn parse_line(line: &str) -> (Vec<&str>, Vec<&str>) {
    let split = line.split(" | ").collect::<Vec<_>>();

    (split[0].split(" ").collect(), split[1].split(" ").collect())
}

fn parse_input(input: &String) -> Vec<(Vec<&str>, Vec<&str>)> {
    input.lines().map(parse_line).collect()
}

pub fn part_1(input: &String) -> usize {
    let parsed = parse_input(input);
    parsed
        .iter()
        .flat_map(|(_, out)| out)
        .map(|x| x.len())
        .filter(|&x| x == 2 || x == 3 || x == 4 || x == 7)
        .count()
}

fn brute(inputs: &Vec<&str>, outputs: &Vec<&str>) -> usize {
    let mut to_check = HashSet::new();
    for c in inputs.into_iter().chain(outputs) {
        to_check.extend(c.chars())
    }

    let mut inputs_of_len: HashMap<usize, Vec<&str>> = HashMap::new();

    for i in 0..10 {
        inputs_of_len.insert(
            i,
            inputs
                .clone()
                .into_iter()
                .filter(|&x| x.len() == i)
                .collect(),
        );
    }
    let mut valids = Vec::new();
    for p in to_check.iter().permutations(to_check.len()) {
        // println!("??? {:?}", &p);
        if !verify_permut(&inputs_of_len, &p) {
            continue;
        }

        valids.push(p);
    }

    assert_eq!(valids.len(), 1);
    let valid = valids[0].clone();

    let mut numbers = Vec::new();
    for &o in outputs {
        let o = o.chars().sorted().collect::<String>();
        for d in DIGITS {
            let mapped_str = d
                .mapped_str_mapping(&valid)
                .chars()
                .sorted()
                .collect::<String>();
            if mapped_str == o {
                numbers.push(d.number)
            }
        }
    }

    numbers
        .iter()
        .map(|x| x.to_string())
        .join("")
        .parse()
        .unwrap()
}

const BASE: [char; 7] = ['a', 'b', 'c', 'd', 'e', 'f', 'g'];

fn verify_permut(inputs_of_len: &HashMap<usize, Vec<&str>>, permut: &Vec<&char>) -> bool {
    let contains = |strs: &Vec<&str>, chars: &Vec<&char>| -> bool {
        strs.iter().all(|&s| chars.iter().all(|&c| s.contains(*c)))
    };

    let mut char_mapping = HashMap::new();
    for (i, &c) in permut.iter().enumerate() {
        char_mapping.insert(BASE[i], c);
    }

    let mut first_preds: Vec<(usize, Vec<&char>)> = Vec::new();

    first_preds.push((2, vec![permut[2], permut[5]])); // 1
    first_preds.push((4, vec![permut[1], permut[2], permut[3], permut[5]])); // 4
    first_preds.push((3, vec![permut[0], permut[2], permut[5]]));

    if !first_preds
        .iter()
        .all(|(s, c)| contains(&inputs_of_len[s], c))
    {
        return false;
    }

    let mut sixes = inputs_of_len[&6].clone();

    for l in ["abcefg", "abdefg", "abcdfg"] {
        let mut to_remove: Option<usize> = None;
        for (i, &s) in sixes.iter().enumerate() {
            if l.chars().all(|c| s.contains(*char_mapping[&c])) {
                to_remove = Some(i);
                break;
            }
        }

        if let Some(tr) = to_remove {
            sixes.remove(tr);
        } else {
            return false;
        }
    }

    let mut fives = inputs_of_len[&5].clone();

    for l in ["acdeg", "acdfg", "abdfg"] {
        let mut to_remove: Option<usize> = None;
        for (i, &s) in fives.iter().enumerate() {
            if l.chars().all(|c| s.contains(*char_mapping[&c])) {
                to_remove = Some(i);
                break;
            }
        }
        if let Some(tr) = to_remove {
            fives.remove(tr);
        } else {
            return false;
        }
    }

    true
}

pub fn part_2(input: &String) -> usize {
    // let input = &TEST_DATA.to_owned();
    let parsed = parse_input(input);

    parsed.iter().map(|(i, o)| brute(i, o)).sum()
}
