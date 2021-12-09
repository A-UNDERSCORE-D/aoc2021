#[rustfmt::skip]
pub mod days {
    pub mod one;
    pub mod two;
    pub mod three;
    pub mod four;
    pub mod five;
    pub mod six;
    pub mod seven;
    pub mod eight;
    pub mod nine;
}

pub mod aoc_util {
    use std::{
        fs, io,
        time::{Duration, Instant},
    };

    use crate::aoc_util;
    use num;

    pub fn get_data(day: usize) -> io::Result<String> {
        fs::read_to_string(format!("../input/{:02}.input", day))
    }

    pub fn to_string_vec(data: &String) -> Vec<String> {
        data.lines().map(str::to_string).collect()
    }

    pub fn to_sectioned_string_vec(data: &String) -> Vec<String> {
        data.split("\n\n").map(str::to_string).collect()
    }

    pub fn to_int_vec(data: &String) -> Vec<i64> {
        data.lines().map(|s| s.parse().unwrap()).collect()
    }

    pub fn to_int_vec_radix<T: num::Integer>(data: &String, radix: u32) -> Vec<T> {
        data.lines()
            .flat_map(|s| T::from_str_radix(s, radix))
            .collect()
    }

    pub fn run_and_time(f: &dyn Fn(&String) -> String, arg: &String) -> (Duration, String) {
        let t = Instant::now();
        let res = f(arg);
        let t = t.elapsed();

        (t, res)
    }

    #[allow(unused_macros)]
    macro_rules! day {
        ($day_name:ident) => {
            (&days::$day_name::part_1, &days::$day_name::part_2)
        };
    }

    macro_rules! day_str {
        ($day_name:ident) => {
            (&|x| format!("{}", days::$day_name::part_1(x)), &|x| {
                format!("{}", days::$day_name::part_2(x))
            })
        };
    }

    pub fn run_puzzles(to_run: &Vec<usize>) -> Vec<[(Duration, String); 2]> {
        use crate::days;

        let days: Vec<(
            &'static dyn Fn(&String) -> String,
            &'static dyn Fn(&String) -> String,
        )> = vec![
            day_str!(one),
            day_str!(two),
            day_str!(three),
            day_str!(four),
            day_str!(five),
            day_str!(six),
            day_str!(seven),
            day_str!(eight),
            day_str!(nine),
        ];

        let mut out = Vec::<[(Duration, String); 2]>::new();

        for d in to_run {
            let day = days.get(d - 1);
            if let None = day {
                out.push([
                    (Duration::ZERO, "Not found".to_string()),
                    (Duration::ZERO, "Not found".to_string()),
                ]);
                continue;
            }

            let (p1, p2) = day.unwrap();

            let input = aoc_util::get_data(*d);

            if let Err(r) = input {
                println!("Failed to get input for day {}: {}", d, r);
                continue;
            }

            let input = input.expect("Impossible.");

            let to_set = [run_and_time(p1, &input), run_and_time(p2, &input)];

            out.push(to_set)
        }

        out
    }
}
