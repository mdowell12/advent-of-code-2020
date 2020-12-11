from solutions.get_inputs import read_inputs


def run_1(inputs):
    seats = [list(line.strip()) for line in inputs]

    def should_vacate_func(i, j, occupied_seats):
        return num_adjacent_occupied(i, j, occupied_seats) >= 4

    def should_occupy_func(i, j, occupied_seats):
        return num_adjacent_occupied(i, j, occupied_seats) == 0

    i = 0
    while True:
        # print()
        # print(f"Step {i}")
        # print_seats(seats)
        num_occupied, next = next_step(seats, should_occupy_func, should_vacate_func)
        if next == seats:
            return num_occupied
        seats = next
        i += 1

def run_2(inputs):
    seats = [list(line.strip()) for line in inputs]

    def should_vacate_func(i, j, occupied_seats):
        return num_visible_occupied(i, j, occupied_seats) >= 5

    def should_occupy_func(i, j, occupied_seats):
        return num_visible_occupied(i, j, occupied_seats) == 0

    i = 0
    while True:
        print()
        print(f"Step {i}")
        print_seats(seats)
        num_occupied, next = next_step(seats, should_occupy_func, should_vacate_func)
        if next == seats:
            return num_occupied
        seats = next
        i += 1


def next_step(seats, should_occupy_func, should_vacate_func):
    occupied_seats = set((i, j) for i, row in enumerate(seats) for j, seat in enumerate(row) if seat == '#')

    num_occupied = 0
    next = [[i for i in row] for row in seats]

    for i, row in enumerate(seats):
        for j, seat in enumerate(row):
            if seat == "L" and should_occupy_func(i, j, occupied_seats):
                next[i][j] = "#"
                num_occupied += 1
            elif seat == "#":
                if should_vacate_func(i, j, occupied_seats):
                    next[i][j] = "L"
                else:
                    num_occupied += 1
            else:
                pass
    return num_occupied, next

def num_adjacent_occupied(i, j, occupied_seats):
    indices = [
        (i-1, j+1),
        (i, j+1),
        (i+1, j+1),
        (i-1, j),
        (i+1, j),
        (i-1, j-1),
        (i, j-1),
        (i+1, j-1),
    ]
    return sum(1 if i in occupied_seats else 0 for i in indices)

def num_visible_occupied(i, j, occupied_seats):
    $ TODO


def print_seats(seats):
    print("\n".join("".join(row) for row in seats))


def run_2(inputs):
    pass


def run_tests():
    test_inputs = """
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 37:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 26:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(11)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
