from solutions.get_inputs import read_inputs


def run_1(inputs):
    return run(inputs, 2020)


def run_2(inputs):
    return run(inputs, 30000000)


def run(inputs, n):
    starters = [int(i) for i in inputs[0].strip().split(',')]
    seen = {val: i+1 for i, val in enumerate(starters)}

    value = starters[-1]
    for i in range(len(seen) + 1, n+1):
        previous = value
        if value in seen:
            value = i - 1 - seen[value]
        else:
            value = 0
        seen[previous] = i - 1
    return value

def run_tests():
    test_inputs = """
    0,3,6
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 436:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_1 = run_1(["1,3,2"])
    if result_1 != 1:
        raise Exception(f"Test 1.2 did not past, got {result_1}")

    result_1 = run_1(["2,1,3"])
    if result_1 != 10:
        raise Exception(f"Test 1.3 did not past, got {result_1}")

    result_1 = run_1(["1,2,3"])
    if result_1 != 27:
        raise Exception(f"Test 1.4 did not past, got {result_1}")

    result_1 = run_1(["2,3,1"])
    if result_1 != 78:
        raise Exception(f"Test 1.5 did not past, got {result_1}")

    result_1 = run_1(["3,2,1"])
    if result_1 != 438:
        raise Exception(f"Test 1.6 did not past, got {result_1}")

    result_1 = run_1(["3,1,2"])
    if result_1 != 1836:
        raise Exception(f"Test 1.7 did not past, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(15)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
