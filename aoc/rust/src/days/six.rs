pub const TEST_DATA: &str = "3,4,3,1,2";

pub fn run_fish(input: &[usize], days: u32) -> u64 {
    let mut nums: Vec<u64> = vec![0; 9];
    for i in input {
        nums[*i] += 1
    }

    for _day in 0..days {
        let mut new = vec![0; 9];
        for i in (0..9).rev() {
            match i {
                0 => {
                    new[6] += nums[0];
                    new[8] += nums[0];
                }

                _ => {
                    new[i - 1] += nums[i];
                }
            }
        }
        nums = new;
    }

    nums.iter().sum()
}

pub fn part_1(input: &String) -> u64 {
    let data: Vec<usize> = input.split(",").flat_map(str::parse).collect();

    return run_fish(&data, 80);
}

pub fn part_2(input: &String) -> u64 {
    let data: Vec<usize> = input.split(",").flat_map(str::parse).collect();

    return run_fish(&data, 256);
}
