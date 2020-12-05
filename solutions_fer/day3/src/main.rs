use std::io::{self, BufRead};

struct Grid {
    pattern: Vec<Vec<char>>,
    pattern_width: usize,
}

impl Grid {
    pub fn new(pattern: Vec<Vec<char>>) -> Self {
        let width = &pattern.get(0).unwrap().len();
        Grid {
            pattern: pattern,
            pattern_width: *width,
        }
    }

    pub fn element_at(&self, position: &Position) -> Option<&char> {
        self.pattern
            .get(position.row)
            .and_then(|row| row.get(position.col % self.pattern_width))
    }
}

struct Position {
    pub row: usize,
    pub col: usize,
}

impl Position {
    pub fn mv(&mut self, mv: &Move) {
        self.row += mv.down;
        self.col += mv.right;
    }
}

struct Move {
    pub right: usize,
    pub down: usize,
}

fn main() {
    let stdin = io::stdin();
    let rows = stdin
        .lock()
        .lines()
        .map(|elem| elem.unwrap().chars().collect());
    let grid = Grid::new(rows.collect());

    println!(
        "Part 1: {}",
        count_trees(&grid, &Move { right: 3, down: 1 })
    );

    let combo1 = count_trees(&grid, &Move { right: 1, down: 1 });
    let combo2 = count_trees(&grid, &Move { right: 3, down: 1 });
    let combo3 = count_trees(&grid, &Move { right: 5, down: 1 });
    let combo4 = count_trees(&grid, &Move { right: 7, down: 1 });
    let combo5 = count_trees(&grid, &Move { right: 1, down: 2 });

    println!("Part 2: {}", combo1 * combo2 * combo3 * combo4 * combo5);
}

fn count_trees(grid: &Grid, mv: &Move) -> usize {
    let mut trees = 0;
    let mut position = Position { row: 0, col: 0 };
    let mut element = grid.element_at(&position);

    while element.is_some() {
        if element.unwrap() == &'#' {
            trees += 1;
        }

        position.mv(mv);
        element = grid.element_at(&position);
    }

    trees
}
