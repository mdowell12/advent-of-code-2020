use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut adapters: Vec<usize> = stdin
        .lock()
        .lines()
        .map(|elem| elem.unwrap().parse::<usize>().unwrap())
        .collect();
    adapters.push(0); // Outlet
    adapters.sort();
    adapters.push(adapters.last().unwrap() + 3); // Device

    let mut one_jolt = 0;
    let mut three_jolt = 0;
    let mut unbridged_groups: Vec<Vec<usize>> = Vec::new();
    unbridged_groups.push(Vec::new());

    for index in 0..(adapters.len() - 1) {
        let diff = adapters[index + 1] - adapters[index];

        if diff == 3 {
            three_jolt += 1;
            unbridged_groups.push(Vec::<usize>::new());
        } else {
            let last_group = unbridged_groups.last_mut().unwrap();
            last_group.push(diff);
        }

        if diff == 1 {
            one_jolt += 1;
        }
    }

    println!("Part 1: {}", one_jolt * three_jolt);

    println!(
        "Part 2: {}",
        unbridged_groups
            .iter()
            .map(|group| combos_in_group(group, 0))
            .fold(1, |memo, mul| memo * mul)
    );
}

fn combos_in_group(group: &Vec<usize>, start_idx: usize) -> usize {
    if group.len() <= start_idx + 1 {
        return 1;
    }
    if group.len() <= start_idx + 2 {
        return 2;
    }

    let next1 = group[start_idx];
    let next2 = group[start_idx + 1];
    let next3 = group[start_idx + 2];

    let mut result = combos_in_group(group, start_idx + 1);

    if next1 + next2 <= 3 {
        result += combos_in_group(group, start_idx + 2)
    }

    if next1 + next2 + next3 <= 3 {
        result += combos_in_group(group, start_idx + 3)
    }

    result
}
