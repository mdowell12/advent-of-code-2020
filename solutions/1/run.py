from solutions.get_inputs import read_inputs


def run_1(inputs):
    left = 0
    right = 1

    while not does_add_to_x([inputs[left], inputs[right]], 2020):
        if right < len(inputs) - 1:
            right += 1
        else:
            left += 1
            right = left + 1

    return inputs[left] * inputs[right]


def run_2(inputs):
    one = 0
    two = 1
    three = 2

    while not does_add_to_x([inputs[one], inputs[two], inputs[three]], 2020):
        if three < len(inputs) - 1:
            three += 1
        else:
            if two < len(inputs) - 2:
                two += 1
                three = two + 1
            else:
                one += 1
                two = one + 1
                three = two + 1

    return inputs[one] * inputs[two] * inputs[three]


def does_add_to_x(elements, desired):
    return sum(elements) == desired


def run_tests():
    test_inputs = """
    1721
    979
    366
    299
    675
    1456""".strip().split('\n')

    result_1 = run_1([int(i) for i in test_inputs])
    if result_1 != 514579:
        raise Exception(f"Test 1 did not past, got {result}")

    result_2 = run_2([int(i) for i in test_inputs])
    if result_2 != 241861950:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(1)

    result_1 = run_1([int(i) for i in input])
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2([int(i) for i in input])
    print(f"Finished 2 with result {result_2}")
