use std::collections::HashSet;
use std::io::{self, BufRead};
use std::iter::FromIterator;

fn main() {
    let stdin = io::stdin();
    let number_set: HashSet<i32> = HashSet::from_iter(
        stdin
            .lock()
            .lines()
            .map(|elem| elem.unwrap().parse::<i32>().unwrap()),
    );

    let number: &i32 = number_set
        .iter()
        .find(|num| number_set.contains(&(2020 - *num)))
        .unwrap();

    println!("{}", number * (2020 - number));
}
