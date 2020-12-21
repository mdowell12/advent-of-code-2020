from collections import defaultdict
from math import sqrt

import numpy as np

from solutions.get_inputs import read_inputs


class Grid(object):

    def __init__(self, tiles):
        self.tiles = {t.id: t for t in tiles}
        # import pdb; pdb.set_trace()
        self.grid_size = int(sqrt(len(tiles)) * (tiles[0].array[0].size - 1))

    def id_to_neighbors(self):
        borders = {}
        for tile in self.tiles.values():
            for border in tile.borders():
                key = ''.join(border)
                if key in borders:
                    borders[key].append(tile.id)
                elif key[::-1] in borders:
                    borders[key[::-1]].append(tile.id)
                else:
                    borders[key] = [tile.id]

        if any(len(v) > 2 for v in borders.values()):
            raise Exception("no way")

        id_to_neighbors = defaultdict(list)
        for border, tile_ids in borders.items():
            for tile_id in tile_ids:
                neighbors = [i for i in tile_ids if i != tile_id]
                id_to_neighbors[tile_id] += neighbors
        return id_to_neighbors

    def assemble(self):
        id_to_neighbors = self.id_to_neighbors()
        # import pdb; pdb.set_trace()
        queue = [i for i in id_to_neighbors if len(id_to_neighbors[i]) == 2][0]
        done = set()
        grid = np.array([['.'] * self.grid_size] * self.grid_size)
        import pdb; pdb.set_trace()
        while queue:
            tile = queue.pop(0)
            if tile.id in done:
                continue
            done.add(tile.id)
            if grid is None:
                grid = tile.array
            for neighbor_id in id_to_neighbors[tile.id]:
                neighbor = self.tiles[neighbor_id]
                grid = add_neighbor_to_grid(tile, neighbor, grid)
        return grid

    def add_neighbor_to_grid(self, tile, neighbor, grid):
        pass

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
    grid = Grid(tiles)
    corners = [id for id, neighbors in grid.id_to_neighbors().items() if len(neighbors) == 2]
    return corners[0] * corners[1] * corners[2] * corners[3]



def run_2(inputs):
    tiles = parse_input(inputs)
    grid = Grid(tiles)
    grid.assemble()


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

    result_2 = run_2(test_inputs)
    if result_2 != 273:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(20)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
