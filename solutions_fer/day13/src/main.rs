use std::collections::HashMap;
use std::convert::TryFrom;
use std::io::{self, BufRead};

struct Bus {
    id: usize,
    offset: usize,
}

impl Bus {
    pub fn matches_timestamp(&self, timestamp: usize) -> bool {
        let res = (timestamp + self.offset) % self.id == 0;
        if res {
            println!(
                "(found ({} + {}) == {} * {})",
                timestamp,
                self.offset,
                self.id,
                (timestamp + self.offset) / self.id
            )
        }
        res
    }
}

fn main() {
    let stdin = io::stdin();
    let mut lines_iter = stdin.lock().lines();
    let timestamp = lines_iter
        .next()
        .unwrap()
        .unwrap()
        .parse::<usize>()
        .unwrap();
    let all_buses_line = lines_iter.next().unwrap().unwrap();
    let all_buses = all_buses_line.split(",");
    let mut buses: Vec<Bus> = all_buses
        .enumerate()
        .filter(|(_, bus)| *bus != "x")
        .map(|(idx, bus)| Bus {
            id: bus.parse::<usize>().unwrap(),
            offset: idx,
        })
        .collect();

    let mut next_buses = HashMap::<usize, usize>::new();

    for bus in buses.iter() {
        let times = (timestamp as f32 / bus.id as f32).ceil() as usize;
        next_buses.insert(times * bus.id, bus.id);
    }
    let next_bus = next_buses.keys().min().unwrap();

    println!(
        "Part 1: {}",
        next_buses.get(next_bus).unwrap() * (next_bus - timestamp)
    );

    buses.sort_by_key(|bus| isize::try_from(bus.id).unwrap() * -1);

    let mut current_candidate = 1;
    let mut current_step = 1;
    for bus in buses.iter() {
        let mut bus_departures = (current_candidate..).step_by(current_step);
        current_candidate = bus_departures
            .find(|dep| bus.matches_timestamp(*dep))
            .unwrap();
        let next_matching_departure = bus_departures
            .find(|dep| bus.matches_timestamp(*dep))
            .unwrap();
        current_step = next_matching_departure - current_candidate;
        println!(
            "==> Candidate for bus {} with offset {}: {}. Next valid candidates in steps of: {}
            ",
            bus.id, bus.offset, current_candidate, current_step
        );
    }

    println!("Part 2: {}", current_candidate);
}
