use std::collections::HashMap;
use std::io::{self, BufRead};
extern crate regex;
use regex::Regex;

struct Program<'a> {
    lines: &'a Vec<Line>,
    memory: HashMap<u64, u64>,
}

enum Line {
    Mask(Mask),
    Mem(Mem),
}

struct Mask {
    chars: Vec<char>,
}

impl Mask {
    pub fn default1() -> Self {
        Self { chars: vec![] }
    }

    pub fn default2() -> Self {
        Self {
            chars: std::iter::repeat('0').take(64).collect(),
        }
    }

    pub fn to_and_or_combo(&self) -> (u64, u64) {
        let mut and = std::u64::MAX;
        let mut or: u64 = 0;

        for bit in self.chars.iter() {
            and <<= 1;
            and += 1;
            or <<= 1;
            match bit {
                '0' => and -= 1,
                '1' => or += 1,
                _ => (),
            }
        }

        (and, or)
    }

    pub fn floating_addresses(&self, mut address: u64) -> Vec<u64> {
        let mut and = std::u64::MAX;
        let mut or: u64 = 0;

        for bit in self.chars.iter() {
            and <<= 1;
            and += 1;
            or <<= 1;
            match bit {
                'X' => and -= 1,
                '1' => or += 1,
                _ => (),
            }
        }

        address &= and;
        address |= or;

        let mut addresses = vec![address];

        for (idx, bit) in self.chars.iter().rev().enumerate() {
            if bit == &'X' {
                let comp = 2_u64.pow(idx as u32);
                let mut new_addresses = vec![];
                for address in addresses {
                    new_addresses.push(address);
                    new_addresses.push(address + comp);
                }
                addresses = new_addresses
            }
        }

        addresses
    }
}

struct Mem {
    address: u64,
    value: u64,
}

impl<'a> Program<'a> {
    pub fn run1(&mut self) {
        let default_mask = Mask::default1();
        let mut current_mask = &default_mask;

        for line in self.lines {
            match line {
                Line::Mask(mask) => current_mask = mask,
                Line::Mem(mem) => {
                    let mut value = mem.value;
                    let (and_mask, or_mask) = current_mask.to_and_or_combo();
                    value &= and_mask;
                    value |= or_mask;
                    self.memory.insert(mem.address, value);
                }
            }
        }
    }

    pub fn run2(&mut self) {
        let default_mask = Mask::default2();
        let mut current_mask = &default_mask;

        for line in self.lines {
            match line {
                Line::Mask(mask) => current_mask = mask,
                Line::Mem(mem) => {
                    for address in current_mask.floating_addresses(mem.address) {
                        self.memory.insert(address, mem.value);
                    }
                }
            }
        }
    }
}

fn main() {
    let mask_re = Regex::new(r"^mask = (?P<mask>.+)$").unwrap();
    let mem_re = Regex::new(r"^mem\[(?P<address>\d+)\] = (?P<value>\d+)").unwrap();

    let stdin = io::stdin();
    let lines: Vec<Line> = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap())
        .map(|line| {
            if mask_re.is_match(&line) {
                Line::Mask(Mask {
                    chars: mask_re
                        .captures(&line)
                        .unwrap()
                        .name("mask")
                        .unwrap()
                        .as_str()
                        .chars()
                        .collect(),
                })
            } else {
                let captures = mem_re.captures(&line).unwrap();

                Line::Mem(Mem {
                    address: captures
                        .name("address")
                        .unwrap()
                        .as_str()
                        .parse::<u64>()
                        .unwrap(),
                    value: captures
                        .name("value")
                        .unwrap()
                        .as_str()
                        .parse::<u64>()
                        .unwrap(),
                })
            }
        })
        .collect();

    let mut program = Program {
        lines: &lines,
        memory: HashMap::new(),
    };
    program.run1();
    println!("Part 1: {}", program.memory.values().sum::<u64>());

    program = Program {
        lines: &lines,
        memory: HashMap::new(),
    };
    program.run2();
    println!("Part 1: {}", program.memory.values().sum::<u64>());
}
