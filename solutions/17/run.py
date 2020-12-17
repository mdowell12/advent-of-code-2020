from solutions.get_inputs import read_inputs


def run_1(inputs):
    positions = {}
    for x, line in enumerate(inputs):
        for y, val in enumerate(line.strip()):
            positions[(x, y, 0)] = val

    print(total_active(positions))
    print()

    turns = 6
    for _ in range(turns):
        positions = iterate_positions(positions)
        print(total_active(positions))
        print()
    return total_active(positions)

def run_2(inputs):
    positions = {}
    for x, line in enumerate(inputs):
        for y, val in enumerate(line.strip()):
            positions[(x, y, 0, 0)] = val

    print(total_active(positions))
    print()

    turns = 6
    for _ in range(turns):
        positions = iterate_positions_2(positions)
        print(total_active(positions))
        print()
    return total_active(positions)


def total_active(positions):
    return sum([1 if val == '#' else 0 for val in positions.values()])


def iterate_positions(positions):
    result = {}
    for position, value in positions.items():
        neighbors = get_neighbors(position, positions)
        new_value = result.get(position, calculate_new_value(position, value, positions, neighbors))
        result[position] = new_value
        for neighbor, neighbor_value in neighbors:
            these_neighbors = get_neighbors(neighbor, positions)
            new_neighbor_value = result.get(neighbor, calculate_new_value(neighbor, neighbor_value, positions, these_neighbors))
            result[neighbor] = new_neighbor_value

    return result


def iterate_positions_2(positions):
    result = {}
    for position, value in positions.items():
        neighbors = get_neighbors_2(position, positions)
        new_value = result.get(position, calculate_new_value(position, value, positions, neighbors))
        result[position] = new_value
        for neighbor, neighbor_value in neighbors:
            these_neighbors = get_neighbors_2(neighbor, positions)
            new_neighbor_value = result.get(neighbor, calculate_new_value(neighbor, neighbor_value, positions, these_neighbors))
            result[neighbor] = new_neighbor_value

    return result


def calculate_new_value(position, value, positions, neighbors):
    num_active_neighbors = sum(1 for (_, val) in neighbors if val == '#')
    if value == '#':
        return '#' if num_active_neighbors in set([2, 3]) else '.'
    else:
        return '#' if num_active_neighbors == 3 else '.'


def get_neighbors(position, positions):
    result = []
    pos_x, pos_y, pos_z = position
    for x in range(pos_x-1, pos_x+2):
        for y in range(pos_y-1, pos_y+2):
            for z in range(pos_z-1, pos_z+2):
                if x == pos_x and y == pos_y and z == pos_z:
                    continue
                neighbor = (x, y, z)
                value = positions.get(neighbor, '.')
                result.append((neighbor, value))
    return result


def get_neighbors_2(position, positions):
    result = []
    pos_x, pos_y, pos_z, pos_w = position
    for x in range(pos_x-1, pos_x+2):
        for y in range(pos_y-1, pos_y+2):
            for z in range(pos_z-1, pos_z+2):
                for w in range(pos_w-1, pos_w+2):
                    if x == pos_x and y == pos_y and z == pos_z and w == pos_w:
                        continue
                    neighbor = (x, y, z, w)
                    value = positions.get(neighbor, '.')
                    result.append((neighbor, value))
    return result


def run_tests():
    positions = {(0, 0, 0): '.', (0, 1, 0): '#', (0, 2, 0): '.', (1, 0, 0): '.', (1, 1, 0): '.', (1, 2, 0): '#', (2, 0, 0): '#', (2, 1, 0): '#', (2, 2, 0): '#'}
    expected = [((-1, -1, -1), '.'), ((-1, -1, 0), '.'), ((-1, -1, 1), '.'), ((-1, 0, -1), '.'), ((-1, 0, 0), '.'), ((-1, 0, 1), '.'), ((-1, 1, -1), '.'), ((-1, 1, 0), '.'), ((-1, 1, 1), '.'), ((0, -1, -1), '.'), ((0, -1, 0), '.'), ((0, -1, 1), '.'), ((0, 0, -1), '.'), ((0, 0, 1), '.'), ((0, 1, -1), '.'), ((0, 1, 0), '#'), ((0, 1, 1), '.'), ((1, -1, -1), '.'), ((1, -1, 0), '.'), ((1, -1, 1), '.'), ((1, 0, -1), '.'), ((1, 0, 0), '.'), ((1, 0, 1), '.'), ((1, 1, -1), '.'), ((1, 1, 0), '.'), ((1, 1, 1), '.')]
    if get_neighbors((0,0,0), positions) != expected:
        raise Exception("get_neighbors test did not pass")

    test_inputs = """
    .#.
    ..#
    ###
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 112:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 848:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(17)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
