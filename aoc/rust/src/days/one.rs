use crate::aoc_util;

pub fn part_1(input: &String) -> usize {
    let data = aoc_util::to_int_vec(input);
    data.windows(2).map(|x| x[1] > x[0]).filter(|x| *x).count()
}

pub fn part_2(input: &String) -> usize {
    let data = aoc_util::to_int_vec(input);

    data.windows(3)
        .zip(data.windows(3).skip(1))
        .map(|(a, b)| b.iter().sum::<i64>() > a.iter().sum())
        .filter(|x| *x)
        .count()
}
