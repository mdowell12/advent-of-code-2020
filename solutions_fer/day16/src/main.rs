use std::collections::HashMap;
use std::io::{self, BufRead};
use std::ops::RangeInclusive;
extern crate regex;
use regex::Regex;

struct Rule {
    name: String,
    first_range: RangeInclusive<usize>,
    second_range: RangeInclusive<usize>,
}

impl Rule {
    pub fn passes(&self, num: &usize) -> bool {
        self.first_range.contains(num) || self.second_range.contains(num)
    }
}

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    let mut rules = Vec::<Rule>::new();

    let rule_re =
        Regex::new(r"^(?P<name>.+): (?P<first_range>.+) or (?P<second_range>.+)$").unwrap();
    loop {
        let rule_line = lines.next().unwrap().unwrap();
        if rule_line == "" {
            break;
        }
        let captures = rule_re.captures(&rule_line).unwrap();
        let name = captures.name("name").unwrap().as_str();
        let mut first_range = captures.name("first_range").unwrap().as_str().split("-");
        let mut second_range = captures.name("second_range").unwrap().as_str().split("-");

        let first_range_a = first_range.next().unwrap().parse::<usize>().unwrap();
        let first_range_b = first_range.next().unwrap().parse::<usize>().unwrap();
        let second_range_a = second_range.next().unwrap().parse::<usize>().unwrap();
        let second_range_b = second_range.next().unwrap().parse::<usize>().unwrap();

        rules.push(Rule {
            name: name.to_string(),
            first_range: (first_range_a..=first_range_b),
            second_range: (second_range_a..=second_range_b),
        });
    }

    lines.next().unwrap().unwrap(); // your ticket:
    let my_ticket: Vec<usize> = lines
        .next()
        .unwrap()
        .unwrap()
        .split(",")
        .map(|num| num.parse::<usize>().unwrap())
        .collect();

    lines.next().unwrap().unwrap(); // empty line
    lines.next().unwrap().unwrap(); // nearby tickets:

    let other_tickets: Vec<Vec<usize>> = lines
        .map(|line| {
            line.unwrap()
                .split(",")
                .map(|num| num.parse::<usize>().unwrap())
                .collect::<Vec<usize>>()
        })
        .collect::<Vec<Vec<usize>>>();

    let mut invalid_nums = Vec::<usize>::new();

    for ticket in other_tickets.iter() {
        for num in ticket {
            if rules.iter().all(|rule| !rule.passes(num)) {
                invalid_nums.push(*num);
            }
        }
    }

    println!("Part 1: {}", invalid_nums.iter().sum::<usize>());

    let mut valid_tickets = Vec::<&Vec<usize>>::new();
    for ticket in other_tickets.iter() {
        if ticket
            .iter()
            .all(|num| rules.iter().any(|rule| rule.passes(num)))
        {
            valid_tickets.push(ticket);
        }
    }

    let mut found_rules = HashMap::<usize, &Rule>::new();
    while found_rules.len() != rules.len() {
        for rule in rules.iter() {
            let possible_columns = (0..my_ticket.len())
                .filter(|idx| !found_rules.contains_key(&idx))
                .filter(|idx| {
                    valid_tickets
                        .iter()
                        .all(|ticket| rule.passes(&ticket[*idx]))
                })
                .collect::<Vec<usize>>();

            if possible_columns.len() == 1 {
                let column = *possible_columns.first().unwrap();
                found_rules.insert(column, rule);
            }
        }
    }

    let mut multiplied = 1;
    for idx in 0..my_ticket.len() {
        let rule = found_rules.get(&idx).unwrap();
        if rule.name.starts_with("departure") {
            multiplied *= my_ticket[idx];
        }
    }

    println!("Part 2: {}", multiplied);
}
