from collections import defaultdict

from solutions.get_inputs import read_inputs


class Tile:

    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, directions):
        for direction in directions:
            if direction == 'e':
                self.x += 2
            elif direction == 'w':
                self.x += -2
            elif direction == 'ne':
                self.x += 1
                self.y += 1
            elif direction == 'nw':
                self.x += -1
                self.y += 1
            elif direction == 'se':
                self.x += 1
                self.y += -1
            elif direction == 'sw':
                self.x += -1
                self.y += -1
            else:
                Exception(direction)
        return self

    def position(self):
        return (self.x, self.y)

    @staticmethod
    def adjacents(x, y):
        return [
            (x + 2, y),
            (x - 2, y),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
        ]

    @staticmethod
    def num_adjacent_black(x, y, grid):
        neighbors = Tile.adjacents(x, y)
        num_black = 0
        for neighbor in neighbors:
            if grid[neighbor] == -1:
                num_black += 1
        return num_black


    def __repr__(self):
        return f"({self.x}, {self.y})"


def run_1(inputs):
    raw_directions = [parse_raw(i) for i in inputs]
    tiles = [Tile().move(i) for i in raw_directions]
    grid = defaultdict(lambda: 1)
    for tile in tiles:
        grid[tile.position()] *= -1

    return len([tile for tile, value in grid.items() if value == -1])



def run_2(inputs):
    raw_directions = [parse_raw(i) for i in inputs]
    tiles = [Tile().move(i) for i in raw_directions]
    grid = defaultdict(lambda: 1)
    for tile in tiles:
        grid[tile.position()] *= -1
    print_grid(grid)
    for i in range(100):
        # Copy grid since we will mutate it
        new_grid = defaultdict(lambda: 1)
        for position, value in grid.items():
            new_grid[position] = value

        black_tiles = [tile for tile, value in grid.items() if value == -1]
        tiles_to_check = set(black_tiles).union(set(tile for x, y in black_tiles for tile in Tile.adjacents(x, y)))
        for position in tiles_to_check:
            x, y = position
            value = grid[position]
            if value == 1:
                # while tile
                if Tile.num_adjacent_black(x, y, grid) == 2:
                    new_grid[position] = -1
            else:
                # black tile
                if Tile.num_adjacent_black(x, y, grid) in (0, 3, 4, 5, 6):
                    new_grid[position] = 1

        grid = defaultdict(lambda: 1)
        for position, value in new_grid.items():
            grid[position] = value

        print(i, len([tile for tile, value in grid.items() if value == -1]))
        print_grid(grid)

    return len([tile for tile, value in grid.items() if value == -1])


def print_grid(grid):
    max_x = max(abs(i) for i, _ in grid)
    max_y = max(abs(i) for _, i in grid)
    rows = []
    for j in range(max_y+1, -max_y, -1):
        row = ''
        for col in range(-max_x, max_x+1):
            if j == col == 0:
                row += 'X' if grid[(col, j)] == -1 else 'O'
            else:
                row += 'x' if grid[(col, j)] == -1 else '.'
        rows.append(row)
    print('\n'.join(rows))


def parse_raw(line):
    letters = list(line.strip())
    result = []
    while letters:
        letter = letters.pop(0)
        if letter in ('e', 'w'):
            result.append(letter)
        else:
            next_letter = letters.pop(0)
            result.append(letter + next_letter)
    return result

def run_tests():
    test_inputs = """
    sesenwnenenewseeswwswswwnenewsewsw
    neeenesenwnwwswnenewnwwsewnenwseswesw
    seswneswswsenwwnwse
    nwnwneseeswswnenewneswwnewseswneseene
    swweswneswnenwsewnwneneseenw
    eesenwseswswnenwswnwnwsewwnwsene
    sewnenenenesenwsewnenwwwse
    wenwwweseeeweswwwnwwe
    wsweesenenewnwwnwsenewsenwwsesesenwne
    neeswseenwwswnwswswnw
    nenwswwsewswnenenewsenwsenwnesesenew
    enewnwewneswsewnwswenweswnenwsenwsw
    sweneswneswneneenwnewenewwneswswnese
    swwesenesewenwneswnwwneseswwne
    enesenwswwswneneswsenwnewswseenwsese
    wnwnesenesenenwwnenwsewesewsesesew
    nenewswnwewswnenesenwnesewesw
    eneswnwswnwsenenwnwnwwseeswneewsenese
    neswnwewnwnwseenwseesewsenwsweewe
    wseweeenwnesenwwwswnew
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 10:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 2208:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(24)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
