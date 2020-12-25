from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    raw_directions = [parse_raw(i) for i in inputs]
    normalized = [normalize(i) for i in raw_directions]
    import pdb; pdb.set_trace()
    tiles_flipped = defaultdict(lambda: 0)
    for tile in normalized:
        tiles_flipped[tile] += 1

    return len([tile for tile, times_flipped in tiles_flipped.items() if times_flipped % 2 != 0])



def run_2(inputs):
    pass


def normalize(directions):
    counts = defaultdict(lambda: 0)
    for direction in directions:
        counts[direction] += 1

    counts['e'] = counts['e'] - counts['w']
    counts['w'] = 0
    counts['ne'] = counts['ne'] - counts['sw']
    counts['sw'] = 0
    counts['nw'] = counts['nw'] - counts['se']
    counts['se'] = 0
    print(counts)
    normalized = ''
    normalized += 'e' * counts['e'] if counts['e'] > 0 else 'w' * (-1 * counts['e'])
    normalized += 'ne' * counts['ne'] if counts['ne'] > 0 else 'sw' * (-1 * counts['ne'])
    normalized += 'nw' * counts['nw'] if counts['nw'] > 0 else 'se' * (-1 * counts['nw'])
    # if counts['ne'] < 0:
    #     import pdb; pdb.set_trace()
    return normalized



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

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(24)

    result_1 = run_1(input)
    # 151 is too low
    # 451 is too high
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
