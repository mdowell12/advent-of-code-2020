use std::io::{self, BufRead};

#[derive(std::cmp::PartialEq, Copy, std::clone::Clone)]
enum Cell {
    Active,
    Inactive,
}

struct Cube {
    cells: Vec<Vec<Vec<Cell>>>,
}

impl Cube {
    pub fn empty(x: usize, y: usize, z: usize) -> Self {
        let cells: Vec<Vec<Vec<Cell>>> = (0..x)
            .map(|_| {
                (0..y)
                    .map(|_| (0..z).map(|_| Cell::Inactive).collect())
                    .collect()
            })
            .collect();

        Self { cells }
    }

    pub fn next(&self) -> Self {
        let (x_size, y_size, z_size) = self.sizes();

        let mut cells: Vec<Vec<Vec<Cell>>> = (0..x_size)
            .map(|_| {
                (0..y_size)
                    .map(|_| (0..z_size).map(|_| Cell::Inactive).collect())
                    .collect()
            })
            .collect();

        for x in 1..(x_size - 1) {
            let slice = &self.cells[x];
            for y in 1..(y_size - 1) {
                let row = &slice[y];
                for z in 1..(z_size - 1) {
                    let cell = &row[z];
                    let active_neighbors = self
                        .neighbors(x, y, z)
                        .iter()
                        .filter(|cell| **cell == Cell::Active)
                        .count();

                    if *cell == Cell::Active && (active_neighbors == 2 || active_neighbors == 3) {
                        cells[x][y][z] = Cell::Active;
                    } else if *cell == Cell::Inactive && active_neighbors == 3 {
                        cells[x][y][z] = Cell::Active;
                    } else {
                        cells[x][y][z] = Cell::Inactive;
                    }
                }
            }
        }

        Self { cells }
    }

    fn neighbors(&self, x: usize, y: usize, z: usize) -> Vec<Cell> {
        let mut cells = Vec::<Cell>::new();

        for x_offset in 0..=2 {
            for y_offset in 0..=2 {
                for z_offset in 0..=2 {
                    if x_offset == 1 && y_offset == 1 && z_offset == 1 {
                        continue;
                    }

                    let cell = self.cells[x + x_offset - 1][y + y_offset - 1][z + z_offset - 1];
                    cells.push(cell);
                }
            }
        }

        cells
    }

    pub fn active_count(&self) -> usize {
        self.cells
            .iter()
            .map(|slice| {
                slice
                    .iter()
                    .map(|row| row.iter().filter(|cell| **cell == Cell::Active).count())
                    .sum::<usize>()
            })
            .sum::<usize>()
    }

    fn sizes(&self) -> (usize, usize, usize) {
        (
            self.cells.len(),
            self.cells[0].len(),
            self.cells[0][0].len(),
        )
    }
}

struct Hypercube {
    cells: Vec<Vec<Vec<Vec<Cell>>>>,
}

impl Hypercube {
    pub fn empty(x: usize, y: usize, z: usize, w: usize) -> Self {
        let cells: Vec<Vec<Vec<Vec<Cell>>>> = (0..x)
            .map(|_| {
                (0..y)
                    .map(|_| {
                        (0..z)
                            .map(|_| (0..w).map(|_| Cell::Inactive).collect())
                            .collect()
                    })
                    .collect()
            })
            .collect();

        Self { cells }
    }

    pub fn next(&self) -> Self {
        let (x_size, y_size, z_size, w_size) = self.sizes();

        let mut cells: Vec<Vec<Vec<Vec<Cell>>>> = (0..x_size)
            .map(|_| {
                (0..y_size)
                    .map(|_| {
                        (0..z_size)
                            .map(|_| (0..w_size).map(|_| Cell::Inactive).collect())
                            .collect()
                    })
                    .collect()
            })
            .collect();

        for x in 1..(x_size - 1) {
            let hyperslice = &self.cells[x];
            for y in 1..(y_size - 1) {
                let slice = &hyperslice[y];
                for z in 1..(z_size - 1) {
                    let row = &slice[z];
                    for w in 1..(w_size - 1) {
                        let cell = &row[w];

                        let active_neighbors = self
                            .neighbors(x, y, z, w)
                            .iter()
                            .filter(|cell| **cell == Cell::Active)
                            .count();

                        if *cell == Cell::Active && (active_neighbors == 2 || active_neighbors == 3)
                        {
                            cells[x][y][z][w] = Cell::Active;
                        } else if *cell == Cell::Inactive && active_neighbors == 3 {
                            cells[x][y][z][w] = Cell::Active;
                        } else {
                            cells[x][y][z][w] = Cell::Inactive;
                        }
                    }
                }
            }
        }

        Self { cells }
    }

    fn neighbors(&self, x: usize, y: usize, z: usize, w: usize) -> Vec<Cell> {
        let mut cells = Vec::<Cell>::new();

        for x_offset in 0..=2 {
            for y_offset in 0..=2 {
                for z_offset in 0..=2 {
                    for w_offset in 0..=2 {
                        if x_offset == 1 && y_offset == 1 && z_offset == 1 && w_offset == 1 {
                            continue;
                        }

                        let cell = self.cells[x + x_offset - 1][y + y_offset - 1][z + z_offset - 1]
                            [w + w_offset - 1];
                        cells.push(cell);
                    }
                }
            }
        }

        cells
    }

    pub fn active_count(&self) -> usize {
        self.cells
            .iter()
            .map(|hyperslice| {
                hyperslice
                    .iter()
                    .map(|slice| {
                        slice
                            .iter()
                            .map(|row| row.iter().filter(|cell| **cell == Cell::Active).count())
                            .sum::<usize>()
                    })
                    .sum::<usize>()
            })
            .sum::<usize>()
    }

    fn sizes(&self) -> (usize, usize, usize, usize) {
        (
            self.cells.len(),
            self.cells[0].len(),
            self.cells[0][0].len(),
            self.cells[0][0][0].len(),
        )
    }
}

fn main() {
    let stdin = io::stdin();
    let char_grid = stdin
        .lock()
        .lines()
        .map(|line| {
            line.unwrap()
                .chars()
                .map(|c| {
                    if c == '#' {
                        Cell::Active
                    } else {
                        Cell::Inactive
                    }
                })
                .collect::<Vec<Cell>>()
        })
        .collect::<Vec<Vec<Cell>>>();

    let x_size = char_grid[0].len();
    let y_size = char_grid.len();
    let z_size = 1;
    let w_size = 1;

    let mut cube = Cube::empty(x_size + 14, y_size + 14, z_size + 14);
    for (x, row) in char_grid.iter().enumerate() {
        for (y, cell) in row.iter().enumerate() {
            cube.cells[x + 6][y + 6][6] = *cell;
        }
    }

    for _ in 0..6 {
        cube = cube.next();
    }

    println!("Part 1: {}", cube.active_count());

    let mut hypercube = Hypercube::empty(x_size + 18, y_size + 18, z_size + 18, w_size + 18);
    for (x, row) in char_grid.iter().enumerate() {
        for (y, cell) in row.iter().enumerate() {
            hypercube.cells[x + 8][y + 8][8][8] = *cell;
        }
    }

    for _ in 0..6 {
        hypercube = hypercube.next();
    }

    println!("Part 2: {}", hypercube.active_count());
}
