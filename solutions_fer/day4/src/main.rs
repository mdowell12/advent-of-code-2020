use std::collections::HashMap;
use std::io::{self, BufRead};
extern crate regex;
use regex::Regex;

const REQUIRED_FIELDS: [&str; 7] = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];

struct Passport {
    fields: HashMap<String, String>,
}

impl Passport {
    pub fn new() -> Self {
        Self {
            fields: HashMap::new(),
        }
    }

    pub fn add_fields(&mut self, line: String) {
        for field in line.split(" ") {
            let mut vals = field.split(":");
            let name = vals.next().unwrap().to_string();
            let value = vals.next().unwrap().to_string();
            self.fields.insert(name, value);
        }
    }

    pub fn is_valid1(&self) -> bool {
        REQUIRED_FIELDS
            .iter()
            .all(|field| self.fields.contains_key(*field))
    }

    pub fn is_valid2(&self) -> bool {
        let valid_byr = self
            .fields
            .get("byr")
            .and_then(|byr| byr.parse::<usize>().ok())
            .and_then(|byr| Some(1920 <= byr && byr <= 2002))
            .unwrap_or(false);
        let valid_iyr = self
            .fields
            .get("iyr")
            .and_then(|iyr| iyr.parse::<usize>().ok())
            .and_then(|iyr| Some(2010 <= iyr && iyr <= 2020))
            .unwrap_or(false);
        let valid_eyr = self
            .fields
            .get("eyr")
            .and_then(|eyr| eyr.parse::<usize>().ok())
            .and_then(|eyr| Some(2020 <= eyr && eyr <= 2030))
            .unwrap_or(false);
        let height_re = Regex::new(r"^((?P<cm>\d+)cm|(?P<inch>\d+)in)$").unwrap();
        let valid_hgt = self
            .fields
            .get("hgt")
            .and_then(|hgt| height_re.captures(hgt))
            .and_then(|caps| {
                Some(
                    caps.name("cm")
                        .and_then(|cm| {
                            Some(
                                150 <= cm.as_str().parse::<usize>().unwrap()
                                    && cm.as_str().parse::<usize>().unwrap() <= 193,
                            )
                        })
                        .unwrap_or(false)
                        || caps
                            .name("inch")
                            .and_then(|inch| {
                                Some(
                                    59 <= inch.as_str().parse::<usize>().unwrap()
                                        && inch.as_str().parse::<usize>().unwrap() <= 76,
                                )
                            })
                            .unwrap_or(false),
                )
            })
            .unwrap_or(false);
        let hair_re = Regex::new(r"^#[a-f0-9]{6}$").unwrap();
        let valid_hcl = self
            .fields
            .get("hcl")
            .and_then(|hcl| Some(hair_re.is_match(hcl)))
            .unwrap_or(false);
        let eyes_re = Regex::new(r"^(amb|blu|brn|gry|grn|hzl|oth)$").unwrap();
        let valid_ecl = self
            .fields
            .get("ecl")
            .and_then(|ecl| Some(eyes_re.is_match(ecl)))
            .unwrap_or(false);
        let pid_re = Regex::new(r"^\d{9}$").unwrap();
        let valid_pid = self
            .fields
            .get("pid")
            .and_then(|pid| Some(pid_re.is_match(pid)))
            .unwrap_or(false);

        valid_byr && valid_iyr && valid_eyr && valid_hgt && valid_hcl && valid_ecl && valid_pid
    }
}

fn main() {
    let stdin = io::stdin();
    let mut passports: Vec<Passport> = vec![Passport::new()];
    for elem in stdin.lock().lines() {
        let line = elem.unwrap();

        if line == "" {
            passports.push(Passport::new());
        } else {
            passports.last_mut().unwrap().add_fields(line)
        }
    }

    println!(
        "Part 1: {}",
        passports
            .iter()
            .filter(|passport| passport.is_valid1())
            .count()
    );

    println!(
        "Part 2: {}",
        passports
            .iter()
            .filter(|passport| passport.is_valid2())
            .count()
    );
}
