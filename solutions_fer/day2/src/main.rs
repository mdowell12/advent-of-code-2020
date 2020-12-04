use std::io::{self, BufRead};

extern crate regex;
use regex::Regex;

struct Password {
    letter: char,
    num1: usize,
    num2: usize,
    string: String,
}

impl Password {
    pub fn is_valid1(&self) -> bool {
        let count = self
            .string
            .chars()
            .filter(|letter| letter == &self.letter)
            .count();

        self.num1 <= count && count <= self.num2
    }

    pub fn is_valid2(&self) -> bool {
        let chars: Vec<char> = self.string.chars().collect();

        (chars.get(self.num1 - 1).unwrap() == &self.letter)
            ^ (chars.get(self.num2 - 1).unwrap() == &self.letter)
    }
}

fn main() {
    let stdin = io::stdin();
    let input_format =
        Regex::new(r"^(?P<num1>\d+)-(?P<num2>\d+) (?P<letter>[a-z]): (?P<string>[a-z]+)$").unwrap();
    let passwords: Vec<Password> = stdin
        .lock()
        .lines()
        .map(|elem| {
            let line = &elem.unwrap();
            let caps = input_format.captures(line).unwrap();
            Password {
                letter: caps
                    .name("letter")
                    .unwrap()
                    .as_str()
                    .chars()
                    .next()
                    .unwrap(),
                num1: caps
                    .name("num1")
                    .unwrap()
                    .as_str()
                    .parse::<usize>()
                    .unwrap(),
                num2: caps
                    .name("num2")
                    .unwrap()
                    .as_str()
                    .parse::<usize>()
                    .unwrap(),
                string: caps.name("string").unwrap().as_str().to_string(),
            }
        })
        .collect();

    let valid1_count = passwords.iter().filter(|pass| pass.is_valid1()).count();

    println!("Part 1: {}", valid1_count);

    let valid2_count = passwords.iter().filter(|pass| pass.is_valid2()).count();

    println!("Part 2: {}", valid2_count);
}
