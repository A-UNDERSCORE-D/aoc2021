use std::time::Instant;

use aoc2021::days::six;
fn main() {
    let input: Vec<usize> = six::TEST_DATA.split(",").flat_map(str::parse).collect();
    let t = Instant::now();
    let _res = six::run_fish(&input, 9999999);
    let t = t.elapsed();

    println!("Done! took {:?}", t)
}
