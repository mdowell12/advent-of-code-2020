from math import pow

from solutions.get_inputs import read_inputs


def run_1(inputs):
    seat_ids = [get_seat_id(i.strip()) for i in inputs]
    return max(seat_ids)


def run_2(inputs):
    all_possible_seat_ids = get_all_possible_seat_ids()
    seat_ids = set(get_seat_id(i.strip()) for i in inputs)
    for id in all_possible_seat_ids:
        if id not in seat_ids and id + 1 in seat_ids and id - 1 in seat_ids:
            return id


def get_all_possible_seat_ids():
    from itertools import product
    sets = [
        ['F', 'B'],
        ['F', 'B'],
        ['F', 'B'],
        ['F', 'B'],
        ['F', 'B'],
        ['F', 'B'],
        ['F', 'B'],

        ['R', 'L'],
        ['R', 'L'],
        ['R', 'L'],
    ]
    possible_seats = set(''.join(i) for i in product(*sets))
    return set(get_seat_id(i) for i in possible_seats)


def get_seat_id(line):
    row_id = get_row_id(line)
    col_id = get_col_id(line)
    return row_id * 8 + col_id


def get_row_id(line):
    letters = list(line[:7])
    keep_lower_letter = 'F'
    return find(letters, keep_lower_letter)


def get_col_id(line):
    letters = list(line[7:])
    keep_lower_letter = 'L'
    return find(letters, keep_lower_letter)


def find(letters, keep_lower_letter):
    num_items = int(pow(2, len(letters)))
    possible_items = [i for i in range(num_items)]
    for letter in letters[:-1]:
        midpoint = int((len(possible_items)) / 2)
        if letter == keep_lower_letter:
            possible_items = possible_items[:midpoint]
        else:
            possible_items = possible_items[midpoint:]
    return possible_items[0] if letters[-1] == keep_lower_letter else possible_items[1]


def run_tests():

    res1 = get_seat_id("BFFFBBFRRR")
    if res1 != 567:
        raise Exception(f"Test BFFFBBFRRR did not past, got {res1}")

    res2 = get_seat_id("FFFBBBFRRR")
    if res2 != 119:
        raise Exception(f"Test FFFBBBFRRR did not past, got {res2}")

    res3 = get_seat_id("BBFFBBFRLL")
    if res3 != 820:
        raise Exception(f"Test BBFFBBFRLL did not past, got {res3}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(5)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
