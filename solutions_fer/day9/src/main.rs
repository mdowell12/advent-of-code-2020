use std::collections::HashSet;
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let numbers: Vec<isize> = stdin
        .lock()
        .lines()
        .map(|elem| elem.unwrap().parse::<isize>().unwrap())
        .collect();

    let mut number_set = HashSet::<isize>::new();

    let mut lower_boundary = 0;
    // Load up the initial 25 numbers
    for index in 0..25 {
        number_set.insert(numbers[index]);
    }
    let mut upper_boundary = 24;

    while sum_pair_exists(&number_set, numbers[upper_boundary + 1]) {
        number_set.remove(&numbers[lower_boundary]);
        lower_boundary += 1;
        upper_boundary += 1;
        number_set.insert(numbers[upper_boundary]);
    }

    let bad_number = numbers[upper_boundary + 1];
    println!("Part 1: {}", bad_number);

    lower_boundary = 0;
    upper_boundary = 0;

    loop {
        let range = &numbers[lower_boundary..=upper_boundary];
        let sum = range.iter().sum();

        if bad_number == sum {
            let max = range.iter().max().unwrap();
            let min = range.iter().min().unwrap();

            println!("Part 2: {}", max + min);
            break;
        } else if bad_number > sum {
            upper_boundary += 1;
        } else {
            lower_boundary += 1;
        }
    }
}

fn sum_pair_exists(set: &HashSet<isize>, number: isize) -> bool {
    set.iter().any(|num1| {
        let complementary = number - num1;

        num1 != &complementary && set.contains(&complementary)
    })
}
