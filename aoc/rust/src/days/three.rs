use std::vec;

use crate::aoc_util;

#[inline]
fn get_bit(data: usize, bit: usize, size: usize) -> u8 {
    ((data & 1 << size - bit - 1) >> size - bit - 1)
        .try_into()
        .unwrap()
}

#[inline]
fn bits(input: usize, size: usize) -> Vec<u8> {
    let mut out: Vec<u8> = vec![0; size];

    for i in 0..size {
        out[i] = get_bit(input, i, size);
    }

    out
}

#[inline]
fn bitcount_columns(input: &Vec<usize>, size: usize) -> (Vec<usize>, Vec<usize>) {
    let (mut zeros, mut ones) = (vec![0; size], vec![0; size]);

    for num in input.iter().map(|x| bits(*x, size)) {
        for (i, n) in num.iter().enumerate() {
            if *n == 1 {
                ones[i] += 1;
            } else {
                zeros[i] += 1;
            }
        }
    }

    (zeros, ones)
}

fn _most(input: (Vec<usize>, Vec<usize>)) -> Vec<bool> {
    input
        .0
        .iter()
        .zip(input.1.iter())
        .map(|(a, b)| b > a)
        .collect()
}

pub fn part_1(input: &String) -> usize {
    let count = bitcount_columns(
        &aoc_util::to_int_vec_radix(&input, 2),
        input.lines().take(1).collect::<Vec<_>>()[0].len(),
    );
    let res: Vec<_> = count
        .0
        .iter()
        .zip(count.1)
        .map(|(ones, zeros)| *ones > zeros)
        .collect();
    let (mut gamma, mut epsilon) = (0, 0);

    for more_ones in res {
        let (mut g_add, mut e_add) = (0, 0);

        if more_ones {
            e_add = 1;
        } else {
            g_add = 1;
        }

        gamma = (gamma << 1) + g_add;
        epsilon = (epsilon << 1) + e_add;
    }

    gamma * epsilon
}

pub fn part_2(_input: &String) -> usize {
    0
}
