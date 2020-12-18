use std::collections::HashMap;
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let nums: Vec<usize> = stdin
        .lock()
        .lines()
        .next()
        .unwrap()
        .unwrap()
        .split(",")
        .map(|num| num.parse::<usize>().unwrap())
        .collect();

    println!("Part 1: {}", play(&nums, 2020));
    println!("Part 1: {}", play(&nums, 30_000_000));
}

fn play(nums: &Vec<usize>, target: usize) -> usize {
    let mut turns: Vec<usize> = vec![];
    let mut positions = HashMap::<usize, Vec<usize>>::new();

    for turn in 0..target {
        if turn % 1_000_000 == 0 {
            println!("Analyzing turn {}", turn);
        }

        let num;

        if nums.len() > turn {
            num = nums[turn];
        } else {
            let last_positions = positions.get(turns.last().unwrap()).unwrap();
            if last_positions.len() > 1 {
                let mut last_two = last_positions.iter().rev().take(2);
                let last = last_two.next().unwrap();
                let second_to_last = last_two.next().unwrap();
                num = last - second_to_last;
            } else {
                num = 0;
            }
        }

        turns.push(num);
        positions.entry(num).or_insert(Vec::new()).push(turn);
    }

    *turns.last().unwrap()
}
