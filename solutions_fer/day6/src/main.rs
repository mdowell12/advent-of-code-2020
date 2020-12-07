use std::collections::HashSet;
use std::io::{self, BufRead};
use std::iter::FromIterator;

struct Group {
    pub persons: Vec<String>,
}

impl Group {
    pub fn new() -> Self {
        Self { persons: vec![] }
    }

    pub fn yeses1(&self) -> HashSet<char> {
        let mut yeses: HashSet<char> = HashSet::new();
        for person in self.persons.iter() {
            yeses.extend(person.chars());
        }
        yeses
    }

    pub fn yeses2(&self) -> HashSet<char> {
        let mut question_sets = self
            .persons
            .iter()
            .map(|person| HashSet::from_iter(person.chars()));

        let first = question_sets.next().unwrap();

        question_sets.fold(first, |memo, person| {
            let intersection = memo.intersection(&person);
            HashSet::from_iter(intersection.into_iter().map(|c| *c))
        })
    }
}

fn main() {
    let stdin = io::stdin();
    let mut groups: Vec<Group> = vec![Group::new()];
    for elem in stdin.lock().lines() {
        let line = elem.unwrap();

        if line == "" {
            groups.push(Group::new());
        } else {
            groups.last_mut().unwrap().persons.push(line);
        }
    }

    println!(
        "Part 1: {}",
        groups
            .iter()
            .fold(0, |memo, group| memo + group.yeses1().len())
    );

    println!(
        "Part 2: {}",
        groups
            .iter()
            .fold(0, |memo, group| memo + group.yeses2().len())
    );
}
