// use chrono::prelude::*;
use std::env;

use aoc2021::aoc_util::run_puzzles;
use chrono::Datelike;

fn main() {
    let args: Vec<String> = env::args().collect();
    let date = chrono::Local::now().date();
    let to_run: Vec<usize>;

    let all_requested = args.iter().any(|x| x == "all");

    if date.day() <= 25 && date.month() == 12 && args.len() == 1 {
        to_run = vec![date.day().try_into().unwrap()]
    } else if all_requested || args.len() == 1 {
        to_run = (1..25).collect()
    } else {
        to_run = args.iter().flat_map(|x| x.parse()).collect();
    }

    let results = run_puzzles(&to_run);

    for (day, result) in to_run.iter().zip(results.iter()) {
        let day = day;
        let ((p1_time, p1_res), (p2_time, p2_res)) = (&result[0], &result[1]);
        println!("Day {:02}: Part 1: {} ({:#?})", day, p1_res, p1_time);
        println!("Day {:02}: Part 2: {} ({:#?})", day, p2_res, p2_time);
        println!()
    }
}
