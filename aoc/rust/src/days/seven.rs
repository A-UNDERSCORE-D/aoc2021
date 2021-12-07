fn fuel_use(start: i64, end: i64, exp: bool) -> i64 {
    let step = (start - end).abs();
    if !exp {
        step
    } else {
        step * (step + 1) / 2
    }
}

pub fn part_1(input: &String) -> i64 {
    let positions = input.split(",").flat_map(str::parse).collect::<Vec<i64>>();

    let max = *positions.iter().max().unwrap();
    let min = *positions.iter().min().unwrap();

    (min..max)
        .into_iter()
        .map(|t| positions.iter().map(|p| fuel_use(*p, t, false)).sum())
        .min()
        .unwrap()
}

pub fn part_2(input: &String) -> i64 {
    let positions = input.split(",").flat_map(str::parse).collect::<Vec<i64>>();

    let max = *positions.iter().max().unwrap();
    let min = *positions.iter().min().unwrap();

    (min..max)
        .into_iter()
        .map(|t| positions.iter().map(|p| fuel_use(*p, t, true)).sum())
        .min()
        .unwrap()
}
