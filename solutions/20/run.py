from collections import defaultdict
from math import sqrt

import numpy as np

from solutions.get_inputs import read_inputs


class Grid:

    def __init__(self, tiles):
        self.tiles = {t.id: t for t in tiles}
        self.grid_size = int(sqrt(len(tiles)) * (tiles[0].array[0].size - 1))
        # Assume square
        self.num_tiles_on_side = int(sqrt(len(tiles)))
        self.id_to_neighbors, self.id_to_matching_borders = self._id_to_neighbors()
        self.grid = self.assemble()

    def _id_to_neighbors(self):
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

        id_to_matching_borders = defaultdict(list)
        for border, tile_ids in borders.items():
            if len(tile_ids) == 2:
                for tile_id in tile_ids:
                    id_to_matching_borders[tile_id].append(border)

        id_to_neighbors = defaultdict(list)
        for border, tile_ids in borders.items():
            for tile_id in tile_ids:
                neighbors = [i for i in tile_ids if i != tile_id]
                id_to_neighbors[tile_id] += neighbors
        return id_to_neighbors, id_to_matching_borders

    def assemble(self):
        """
        Returns list of lists of tiles, which can each be accessed by their ids.
        The tiles' arrays are mutated in this function.
        """
        result = []

        corner_id = [i for i in self.id_to_neighbors if len(self.id_to_neighbors[i]) == 2][0]
        corner = self.tiles[corner_id]
        corner.orient_upper_left(self.id_to_matching_borders[corner.id])

        for row in range(self.num_tiles_on_side):
            for col in range(self.num_tiles_on_side):
                if col == 0:
                    if row == 0:
                        # Initialize if empty
                        result.append([corner])
                    else:
                        neighbor_above = result[row-1][col]
                        potential_pieces = self.id_to_neighbors[neighbor_above.id]
                        piece = self.find_matching(neighbor_above.bottom(), potential_pieces)
                        self.orient_matching_above(neighbor_above, piece)
                        result.append([])
                        result[row].append(piece)
                else:
                    neighbor_left = result[row][col-1]
                    potential_pieces = self.id_to_neighbors[neighbor_left.id]
                    piece = self.find_matching(neighbor_left.right(), potential_pieces)
                    self.orient_matching_left(neighbor_left, piece)
                    result[row].append(piece)

        return result

    def find_matching(self, border_to_match, neighbors):
        border_to_match = ''.join(border_to_match)
        for neighbor_id in neighbors:
            neighbor = self.tiles[neighbor_id]
            for border in neighbor.borders():
                if ''.join(border) in (border_to_match, border_to_match[::-1]):
                    return neighbor
        raise Exception(border_to_match + ' ' + str(neighbors))

    def orient_matching_left(self, neighbor_left, piece):
        border_to_match = ''.join(neighbor_left.right())
        while ''.join(piece.left()) not in (border_to_match, border_to_match[::-1]):
            piece.rotate()
        if ''.join(piece.left()) != border_to_match:
            piece.vertical_flip()

    def orient_matching_above(self, neighbor_above, piece):
        border_to_match = ''.join(neighbor_above.bottom())
        while ''.join(piece.top()) not in (border_to_match, border_to_match[::-1]):
            piece.rotate()
        if ''.join(piece.top()) != border_to_match:
            piece.horizontal_flip()

    def remove_borders(self):
        for row in self.grid:
            for tile in row:
                tile.remove_borders()

    def image(self):
        self.remove_borders()
        lines = []
        for row in self.grid:
            for i in range(len(row[0].array[0])):
                line_for_row = []
                for tile in row:
                    line_for_row += list(tile.array[i])
                lines.append(line_for_row)
        return np.array(lines)


    def __repr__(self):
        lines = []
        for row in self.grid:
            lines_for_row = Tile.strs_for_row(row)
            lines += lines_for_row
            lines += '\n'
        return '\n'.join(lines)


class Tile:

    def __init__(self, tile_id, lines):
        self.id = tile_id
        parsed = [list(l.strip()) for l in lines]
        self.array = np.array(parsed)

    def borders(self):
        return [
            self.top(),
            self.left(),
            self.right(),
            self.bottom(),
        ]

    def top(self):    return self.array[0]
    def left(self):   return self.array[:,0]
    def right(self):  return self.array[:,-1]
    def bottom(self): return self.array[-1]

    def rotate(self):
        self.array = np.rot90(self.array)

    def vertical_flip(self):
        self.array = np.flipud(self.array)

    def horizontal_flip(self):
        self.array = np.fliplr(self.array)

    def orient_upper_left(self, borders):
        if len(borders) != 2:
            raise Exception(len(borders))
        right = borders[0]
        while right != ''.join(self.right()):
            if ''.join(self.right())[::-1] == right:
                self.vertical_flip()
                break
            self.rotate()

        if ''.join(self.bottom()) != borders[1]:
            self.vertical_flip()

    def remove_borders(self):
        self.array = self.array[1:, :]
        self.array = self.array[:-1, :]
        self.array = self.array[:, 1:]
        self.array = self.array[:, :-1]

    @staticmethod
    def strs_for_row(tiles):
        lines = []
        for i in range(len(tiles[0].left())):
            line = ''
            for tile in tiles:
                line += ''.join(tile.array[i])
                line += ' '
            lines.append(line)
        return lines

    def __repr__(self):
        return "\n".join("".join(row) for row in self.array)


def run_1(inputs):
    tiles = parse_input(inputs)
    grid = Grid(tiles)
    corners = [id for id, neighbors in grid.id_to_neighbors.items() if len(neighbors) == 2]
    return corners[0] * corners[1] * corners[2] * corners[3]


def run_2(inputs):
    tiles = parse_input(inputs)
    grid = Grid(tiles)
    print(grid)
    image = grid.image()

    total_pounds = total_pound_signs(image)

    # Only one orientation of the image contains the seamonsters
    # Find it with brute force
    for i in range(4):
        rotated = np.rot90(image, i)
        in_seamonster = pound_signs_in_sea_monster(rotated)
        if in_seamonster:
            print_image_with_seamonsters(rotated, in_seamonster)
            return total_pounds - len(in_seamonster)

        flipped = np.fliplr(rotated)
        in_seamonster = pound_signs_in_sea_monster(flipped)
        if in_seamonster:
            print_image_with_seamonsters(flipped, in_seamonster)
            return total_pounds - len(in_seamonster)

    raise Exception("No seamonsters found")


def pound_signs_in_sea_monster(image):
    sea_monster_coordinates = set()
    for i in range(0, len(image) - 2):
        for j in range(18, len(image) - 1):
            sea_monster_coordinates = sea_monster_coordinates.union(
                get_seamonster_coordinates(i, j, image, sea_monster_coordinates)
            )
    return sea_monster_coordinates


def total_pound_signs(image):
    result = 0
    for i in image:
        for j in i:
            if j == '#':
                result += 1
    return result


def get_seamonster_coordinates(i, j, image, already_seamonster):
    potential_seamonster = generate_seamonster(i, j)

    if potential_seamonster.intersection(already_seamonster):
        return set()
    elif all(image[coord] == '#' for coord in potential_seamonster):
        # print(f"Found seamonster at ({i}, {j})")
        return potential_seamonster
    else:
        return set()


def generate_seamonster(i, j):
    return set([
        (i, j),
        (i+1, j-18),
        (i+1, j-13),
        (i+1, j-12),
        (i+1, j-7),
        (i+1, j-6),
        (i+1, j-1),
        (i+1, j),
        (i+1, j+1),
        (i+2, j-17),
        (i+2, j-14),
        (i+2, j-11),
        (i+2, j-8),
        (i+2, j-5),
        (i+2, j-2),
    ])

def print_image_with_seamonsters(image, sea_monster_coordinates):
    lines = []
    for i, row in enumerate(image):
        line = []
        for j, col in enumerate(row):
            # import pdb; pdb.set_trace()
            if (i, j) in sea_monster_coordinates:
                # line.append('O')
                line.append(f"\033[96m0\033[0m")
                # line.append('\N{grinning face with smiling eyes}')
            else:
                line.append(col)
        lines.append(''.join(line))
    print('\n'.join(lines))


def parse_input(inputs):
    copy = [i.strip() for i in inputs if i.strip()]
    tiles = []
    lines = None
    tile_id = None
    while copy:
        next_tile = copy.pop(0)
        if 'Tile' in next_tile:
            if tile_id and lines:
                tiles.append(Tile(tile_id, lines))
            lines = []
            tile_id = int(next_tile[5:-1])
        else:
            lines.append(next_tile)
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
    print("Test 1 passed")

    result_2 = run_2(test_inputs)
    if result_2 != 273:
        raise Exception(f"Test 2 did not past, got {result_2}")
    print("Test 2 passed")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(20)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
