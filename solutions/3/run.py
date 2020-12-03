from solutions.get_inputs import read_inputs


def run_1(inputs):
    return count_trees_for_slope(inputs, 3, 1)


def run_2(inputs):
    result = 1
    result *= count_trees_for_slope(inputs, 1, 1)
    result *= count_trees_for_slope(inputs, 3, 1)
    result *= count_trees_for_slope(inputs, 5, 1)
    result *= count_trees_for_slope(inputs, 7, 1)
    result *= count_trees_for_slope(inputs, 1, 2)
    return result


def count_trees_for_slope(inputs, right_increment, down_increment):
    num_trees = 0

    curr_x = 0
    curr_y = 0

    while curr_y + down_increment < len(inputs):
        curr_x += right_increment
        curr_y += down_increment
        line = inputs[curr_y]
        char = get_character(line, curr_x)
        if is_tree(char):
            num_trees += 1

    return num_trees


def get_character(line, curr_x):
    return line[curr_x % len(line)]


def is_tree(char):
    return char == "#"


def run_tests():
    input_str = """
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#
    """
    test_inputs = [i.strip() for i in input_str.strip().split('\n')]

    result_1 = run_1(test_inputs)
    if result_1 != 7:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 336:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = [i.strip() for i in read_inputs(3)]

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
