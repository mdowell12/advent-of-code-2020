use std::convert::{TryFrom, TryInto};
use std::io::{self, BufRead};

struct Instruction {
    pub action: Action,
    value: usize,
}

enum Action {
    N,
    S,
    E,
    W,
    L,
    R,
    F,
}

struct Ship {
    position: Position,
    orientation: Orientation,
    waypoint_position: Position,
}

struct Position {
    x: isize,
    y: isize,
}

#[derive(std::cmp::PartialEq, Copy, std::clone::Clone)]
enum Orientation {
    N,
    S,
    E,
    W,
}

const ORIENTATIONS: [Orientation; 4] = [
    Orientation::N,
    Orientation::E,
    Orientation::S,
    Orientation::W,
];

impl Ship {
    pub fn new() -> Self {
        Self {
            position: Position { x: 0, y: 0 },
            orientation: Orientation::E,
            waypoint_position: Position { x: 10, y: 1 },
        }
    }

    pub fn run1(&mut self, instruction: &Instruction) {
        let isize_value = isize::try_from(instruction.value).unwrap();

        match instruction.action {
            Action::N => self.position.y += isize_value,
            Action::S => self.position.y -= isize_value,
            Action::E => self.position.x += isize_value,
            Action::W => self.position.x -= isize_value,
            Action::L => self.turn_left(instruction.value),
            Action::R => self.turn_right(instruction.value),
            Action::F => match self.orientation {
                Orientation::N => self.position.x += isize_value,
                Orientation::S => self.position.x -= isize_value,
                Orientation::E => self.position.y += isize_value,
                Orientation::W => self.position.y -= isize_value,
            },
        }
    }

    pub fn run2(&mut self, instruction: &Instruction) {
        let isize_value = isize::try_from(instruction.value).unwrap();

        match instruction.action {
            Action::N => self.waypoint_position.y += isize_value,
            Action::S => self.waypoint_position.y -= isize_value,
            Action::E => self.waypoint_position.x += isize_value,
            Action::W => self.waypoint_position.x -= isize_value,
            Action::L => self.turn_waypoint_left(instruction.value),
            Action::R => self.turn_waypoint_right(instruction.value),
            Action::F => {
                self.position.x += self.waypoint_position.x * isize_value;
                self.position.y += self.waypoint_position.y * isize_value;
            }
        }
    }

    pub fn manhattan_distance(&self) -> usize {
        (self.position.x.abs() + self.position.y.abs())
            .try_into()
            .unwrap()
    }

    fn turn_left(&mut self, value: usize) {
        let steps: isize = (value / 90).try_into().unwrap();
        let new_orientation_index: usize =
            modulo(self.current_orientation_index() - steps, ORIENTATIONS.len());

        self.orientation = ORIENTATIONS[new_orientation_index];
    }

    fn turn_right(&mut self, value: usize) {
        let steps: isize = (value / 90).try_into().unwrap();
        let new_orientation_index: usize =
            modulo(self.current_orientation_index() + steps, ORIENTATIONS.len());

        self.orientation = ORIENTATIONS[new_orientation_index];
    }

    fn turn_waypoint_left(&mut self, value: usize) {
        match value {
            90 => {
                self.waypoint_position = Position {
                    x: -self.waypoint_position.y,
                    y: self.waypoint_position.x,
                }
            }
            180 => {
                self.waypoint_position = Position {
                    x: -self.waypoint_position.x,
                    y: -self.waypoint_position.y,
                }
            }
            270 => {
                self.waypoint_position = Position {
                    x: self.waypoint_position.y,
                    y: -self.waypoint_position.x,
                }
            }
            other => panic!("Surprise angle {}", other),
        }
    }

    fn turn_waypoint_right(&mut self, value: usize) {
        self.turn_waypoint_left(modulo(isize::try_from(value).unwrap() * -1, 360))
    }

    fn current_orientation_index(&self) -> isize {
        ORIENTATIONS
            .iter()
            .position(|&elem| elem == self.orientation)
            .unwrap()
            .try_into()
            .unwrap()
    }
}

fn main() {
    let stdin = io::stdin();
    let instructions: Vec<Instruction> = stdin
        .lock()
        .lines()
        .map(|elem| {
            let line = elem.unwrap();
            let action = match &line[..1] {
                "N" => Action::N,
                "S" => Action::S,
                "E" => Action::E,
                "W" => Action::W,
                "L" => Action::L,
                "R" => Action::R,
                "F" => Action::F,
                other => panic!("Unknown action {}", other),
            };
            let value = line[1..].parse::<usize>().unwrap();

            Instruction { action, value }
        })
        .collect();

    let mut ship1 = Ship::new();

    for instruction in instructions.iter() {
        ship1.run1(instruction);
    }

    println!("Part 1: {}", ship1.manhattan_distance());

    let mut ship2 = Ship::new();

    for instruction in instructions.iter() {
        ship2.run2(instruction);
    }

    println!("Part 2: {}", ship2.manhattan_distance());
}

fn modulo(a: isize, b: usize) -> usize {
    let isize_b = isize::try_from(b).unwrap();

    usize::try_from((a % isize_b) + isize_b).unwrap() % b
}
