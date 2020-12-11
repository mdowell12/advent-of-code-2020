from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    jolts = sorted([int(i) for i in inputs])
    jolts = [0] + jolts + [jolts[-1] + 3]
    diffs = defaultdict(lambda: 0)
    for i, jolt in enumerate(jolts):
        if i == 0:
            continue
        diffs[jolt - jolts[i-1]] += 1

    return diffs[1] * diffs[3]


def run_2(inputs):
    jolts = sorted([int(i) for i in inputs])
    jolts = [0] + jolts + [jolts[-1] + 3]

    chunks = []

    current_chunk = []
    for i, jolt in enumerate(jolts):
        # if start or end, skip
        if i == 0 or i == len(jolts) - 1:
            continue

        before = jolt - jolts[i-1]
        after = jolts[i+1] - jolt
        if before == after == 1:
            current_chunk.append(jolt)
        else:
            # chunk ended
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = []

    result = 1
    for c in chunks:
        num_valid = num_valid_permutations(c)
        print(c, num_valid)
        result *= num_valid
    return result


def num_valid_permutations(c):
    return {
        1: 2,
        2: 4,
        3: 7
    }[len(c)]

    ##########################################################
    # RIP my attempt to do it generally :(
    ##########################################################
    # from math import factorial
    # def n_choose_k(n, k):
    #     return int(factorial(n) / (factorial(k) * (factorial(n - k))))
    # result = 1
    # for k in range(1, len(c) + 1):
    #     num_invalid = 0 if k in {1, 2, 3} else k
    #     result += n_choose_k(len(c), k) - num_invalid
    # print(c, result)
    # return result




def run_tests():
    test_inputs = """
    16
    10
    15
    5
    1
    11
    7
    19
    6
    12
    4
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 35:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 8:
        raise Exception(f"Test 2 did not past, got {result_2}")

    test_inputs = """
    28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 220:
        raise Exception(f"Test 1.2 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 19208:
        raise Exception(f"Test 2.2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(10)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
