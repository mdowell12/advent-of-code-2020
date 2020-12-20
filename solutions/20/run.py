from collections import defaultdict

import numpy as np

from solutions.get_inputs import read_inputs

# TODO update requirements.txt

class Tile(object):

    def __init__(self, id, lines):
        self.id = id
        parsed = [[i for i in l.strip()] for l in lines]
        self.array = np.array(parsed)

    def borders(self):
        return [
            self.array[0],     # top
            self.array[:,0],   # left
            self.array[:,-1],  # right
            self.array[-1],    # bottom
        ]

    def __repr__(self):
        return "\n".join("".join(row) for row in self.array)


def run_1(inputs):
    tiles = parse_input(inputs)
    # import pdb; pdb.set_trace()
    # for tile in tiles:
    #     print(tile.id)
    #     print(tile)
    #     print()
    borders = defaultdict(list)
    # TODO this does not account for flipping a border. i.e. a border appears
    # in the borders dict twice, in both orders
    for tile in tiles:
        for border in tile.borders():
            borders[''.join(border)].append(tile.id)
    print(borders)
    if any(len(v) > 2 for v in borders.values()):
        raise Exception("no way")
    id_to_neighbors = defaultdict(list)
    for border, tile_ids in borders.items():
        for tile_id in tile_ids:
            neighbors = [i for i in tile_ids if i != tile_id]
            id_to_neighbors[tile_id] += neighbors
    print(id_to_neighbors)



def run_2(inputs):
    pass


def parse_input(inputs):
    copy = [i.strip() for i in inputs if i.strip()]
    tiles = []
    lines = None
    tile_id = None
    while copy:
        next = copy.pop(0)
        if 'Tile' in next:
            if tile_id and lines:
                tiles.append(Tile(tile_id, lines))
            lines = []
            tile_id = int(next[5:-1])
        else:
            lines.append(next)
    if tile_id and lines:
        tiles.append(Tile(tile_id, lines))
    return tiles

def run_tests():
    test_inputs = """
    Tile 2311:
    ..##.#..#.
    ##..#.....
    #...##..#.
    ####.#...#
    ##.##.###.
    ##...#.###
    .#.#.#..##
    ..#....#..
    ###...#.#.
    ..###..###

    Tile 1951:
    #.##...##.
    #.####...#
    .....#..##
    #...######
    .##.#....#
    .###.#####
    ###.##.##.
    .###....#.
    ..#.#..#.#
    #...##.#..

    Tile 1171:
    ####...##.
    #..##.#..#
    ##.#..#.#.
    .###.####.
    ..###.####
    .##....##.
    .#...####.
    #.##.####.
    ####..#...
    .....##...

    Tile 1427:
    ###.##.#..
    .#..#.##..
    .#.##.#..#
    #.#.#.##.#
    ....#...##
    ...##..##.
    ...#.#####
    .#.####.#.
    ..#..###.#
    ..##.#..#.

    Tile 1489:
    ##.#.#....
    ..##...#..
    .##..##...
    ..#...#...
    #####...#.
    #..#.#.#.#
    ...#.#.#..
    ##.#...##.
    ..##.##.##
    ###.##.#..

    Tile 2473:
    #....####.
    #..#.##...
    #.##..#...
    ######.#.#
    .#...#.#.#
    .#########
    .###.#..#.
    ########.#
    ##...##.#.
    ..###.#.#.

    Tile 2971:
    ..#.#....#
    #...###...
    #.#.###...
    ##.##..#..
    .#####..##
    .#..####.#
    #..#.#..#.
    ..####.###
    ..#.#.###.
    ...#.#.#.#

    Tile 2729:
    ...#.#.#.#
    ####.#....
    ..#.#.....
    ....#..#.#
    .##..##.#.
    .#.####...
    ####.#.#..
    ##.####...
    ##..#.##..
    #.##...##.

    Tile 3079:
    #.#.#####.
    .#..######
    ..#.......
    ######....
    ####.#..#.
    .#...#.##.
    #.#####.##
    ..#.###...
    ..#.......
    ..#.###...
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 20899048083289:
        raise Exception(f"Test 1 did not past, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(1)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
