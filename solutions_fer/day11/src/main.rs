use std::convert::TryInto;
use std::io::{self, BufRead};

#[derive(std::cmp::PartialEq)]
struct SeatLayout {
    seats: Vec<Vec<SeatType>>,
}

#[derive(std::cmp::PartialEq, std::clone::Clone, Copy)]
enum SeatType {
    Floor,
    Empty,
    Occupied,
}

impl SeatLayout {
    pub fn rule_round1(&self) -> Self {
        let seats: Vec<Vec<SeatType>> = self
            .seats
            .iter()
            .enumerate()
            .map(|(row_idx, row)| {
                row.iter()
                    .enumerate()
                    .map(|(col_idx, seat)| {
                        if *seat == SeatType::Floor {
                            SeatType::Floor
                        } else {
                            let occupied_neighbors = self.count_occupied_neighbors(
                                row_idx.try_into().unwrap(),
                                col_idx.try_into().unwrap(),
                            );

                            if *seat == SeatType::Empty && occupied_neighbors == 0 {
                                SeatType::Occupied
                            } else if *seat == SeatType::Occupied && occupied_neighbors >= 4 {
                                SeatType::Empty
                            } else {
                                *seat
                            }
                        }
                    })
                    .collect()
            })
            .collect();

        Self { seats }
    }

    pub fn rule_round2(&self) -> Self {
        let seats: Vec<Vec<SeatType>> = self
            .seats
            .iter()
            .enumerate()
            .map(|(row_idx, row)| {
                row.iter()
                    .enumerate()
                    .map(|(col_idx, seat)| {
                        if *seat == SeatType::Floor {
                            SeatType::Floor
                        } else {
                            let occupied_seeable_neighbors = self.count_occupied_seeable_neighbors(
                                row_idx.try_into().unwrap(),
                                col_idx.try_into().unwrap(),
                            );

                            if *seat == SeatType::Empty && occupied_seeable_neighbors == 0 {
                                SeatType::Occupied
                            } else if *seat == SeatType::Occupied && occupied_seeable_neighbors >= 5
                            {
                                SeatType::Empty
                            } else {
                                *seat
                            }
                        }
                    })
                    .collect()
            })
            .collect();

        Self { seats }
    }

    pub fn count_occupied(&self) -> usize {
        self.seats
            .iter()
            .map(|row| {
                row.iter()
                    .filter(|cell| **cell == SeatType::Occupied)
                    .count()
            })
            .sum()
    }

    fn count_occupied_neighbors(&self, row_idx: isize, col_idx: isize) -> usize {
        self.count_occupied_cell(row_idx - 1, col_idx - 1)
            + self.count_occupied_cell(row_idx - 1, col_idx)
            + self.count_occupied_cell(row_idx - 1, col_idx + 1)
            + self.count_occupied_cell(row_idx, col_idx - 1)
            + self.count_occupied_cell(row_idx, col_idx + 1)
            + self.count_occupied_cell(row_idx + 1, col_idx - 1)
            + self.count_occupied_cell(row_idx + 1, col_idx)
            + self.count_occupied_cell(row_idx + 1, col_idx + 1)
    }

    fn count_occupied_seeable_neighbors(&self, row_idx: isize, col_idx: isize) -> usize {
        let mut result = 0;

        // Upper left
        let mut row_ptr = row_idx - 1;
        let mut col_ptr = col_idx - 1;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                row_ptr -= 1;
                col_ptr -= 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Up
        row_ptr = row_idx - 1;
        col_ptr = col_idx;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                row_ptr -= 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Upper right
        row_ptr = row_idx - 1;
        col_ptr = col_idx + 1;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                row_ptr -= 1;
                col_ptr += 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Left
        row_ptr = row_idx;
        col_ptr = col_idx - 1;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                col_ptr -= 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Right
        row_ptr = row_idx;
        col_ptr = col_idx + 1;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                col_ptr += 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Lower left
        row_ptr = row_idx + 1;
        col_ptr = col_idx - 1;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                row_ptr += 1;
                col_ptr -= 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Down
        row_ptr = row_idx + 1;
        col_ptr = col_idx;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                row_ptr += 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        // Lower right
        row_ptr = row_idx + 1;
        col_ptr = col_idx + 1;
        loop {
            let seat = self.get_pos(row_ptr, col_ptr);

            if seat == &SeatType::Floor {
                row_ptr += 1;
                col_ptr += 1;
            } else {
                if seat == &SeatType::Occupied {
                    result += 1;
                }
                break;
            }
        }

        result
    }

    fn count_occupied_cell(&self, row_idx: isize, col_idx: isize) -> usize {
        (self.get_pos(row_idx, col_idx) == &SeatType::Occupied) as usize
    }

    fn get_pos(&self, row_idx: isize, col_idx: isize) -> &SeatType {
        if row_idx < 0 || col_idx < 0 {
            return &SeatType::Empty;
        }
        let urow_idx: usize = row_idx.try_into().unwrap();
        let ucol_idx: usize = col_idx.try_into().unwrap();

        self.seats
            .get(urow_idx)
            .and_then(|row| row.get(ucol_idx))
            .unwrap_or(&SeatType::Empty)
    }
}

fn main() {
    let stdin = io::stdin();
    let seats: Vec<Vec<SeatType>> = stdin
        .lock()
        .lines()
        .map(|elem| {
            elem.unwrap()
                .chars()
                .map(|chr| match chr {
                    '.' => SeatType::Floor,
                    'L' => SeatType::Empty,
                    '#' => SeatType::Occupied,
                    other => panic!("Unknown seat type {}", other),
                })
                .collect()
        })
        .collect();

    let mut seat_layout = SeatLayout {
        seats: seats.clone(),
    };
    loop {
        let next_layout = seat_layout.rule_round1();
        if seat_layout == next_layout {
            println!("Part 1: {}", seat_layout.count_occupied());
            break;
        } else {
            seat_layout = next_layout;
        }
    }

    seat_layout = SeatLayout {
        seats: seats.clone(),
    };
    loop {
        let next_layout = seat_layout.rule_round2();
        if seat_layout == next_layout {
            println!("Part 2: {}", seat_layout.count_occupied());
            break;
        } else {
            seat_layout = next_layout;
        }
    }
}
