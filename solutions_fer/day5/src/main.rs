use std::collections::HashSet;
use std::io::{self, BufRead};
use std::iter::FromIterator;

fn main() {
    let stdin = io::stdin();
    let seat_ids = stdin
        .lock()
        .lines()
        .map(|elem| {
            elem.unwrap()
                .replace("F", "0")
                .replace("B", "1")
                .replace("L", "0")
                .replace("R", "1")
        })
        .map(|bp| usize::from_str_radix(&bp, 2).unwrap());
    let seat_ids_set = HashSet::<usize>::from_iter(seat_ids);

    println!("Part 1: {}", (&seat_ids_set).into_iter().max().unwrap());

    for i in 1..(2_usize.pow(10) - 1) {
        if seat_ids_set.contains(&(i - 1))
            && !seat_ids_set.contains(&i)
            && seat_ids_set.contains(&(i + 1))
        {
            println!("Part 2: {}", i);
        }
    }
}
