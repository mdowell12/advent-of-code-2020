use std::collections::HashSet;
use std::io::{self, BufRead};
use std::iter::FromIterator;

fn main() {
    let stdin = io::stdin();
    let numbers = stdin
        .lock()
        .lines()
        .map(|elem| elem.unwrap().parse::<i32>().unwrap());

    let number_set: HashSet<i32> = HashSet::from_iter(numbers);

    for num1 in number_set.iter() {
        for num2 in number_set.iter() {
            let complimentary = 2020 - num1 - num2;

            if number_set.contains(&complimentary) {
                println!("{}", num1 * num2 * complimentary);
                return;
            }
        }
    }
}
