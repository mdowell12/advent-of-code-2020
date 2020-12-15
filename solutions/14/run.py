from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    def set_memory_value(memory, location, value, mask):
        masked_value = apply_mask_1(mask, int(value))
        memory[location] = masked_value
    return run(inputs, set_memory_value)


def run_2(inputs):
    def set_memory_value(memory, location, value, mask):
        value = int(value)
        locations = get_locations(mask, location)
        for l in locations:
            memory[l] = value
    return run(inputs, set_memory_value)


def run(inputs, apply_value_fn):
    memory = defaultdict(lambda x: 0)
    mask = ""
    for line in inputs:
        command, value = line.strip().split(" = ")
        if "mask" in command:
            mask = value
        else:
            location = command[4:-1]
            apply_value_fn(memory, location, value, mask)

    return sum(memory.values())


def apply_mask_1(mask, value):
    num_bits = len(mask)
    binary_value = format(value, "b")
    # pad on left
    binary_value = "0" * (num_bits - len(binary_value)) + binary_value
    # print(mask)
    # print(binary_value)
    # print()
    result = []
    for i, mask_value in enumerate(mask):
        if mask_value == "X":
            result.append(binary_value[i])
        else:
            result.append(mask_value)

    return int("".join(result), 2)


def get_locations(mask, location):
    binary_location = format(int(location), "b")
    # pad on left
    binary_location = "0" * (len(mask) - len(binary_location)) + binary_location
    results = [[]]
    for i, mask_value in enumerate(mask):
        if mask_value == "0":
            for r in results:
                r.append(binary_location[i])
        elif mask_value == "1":
            for r in results:
                r.append("1")
        elif mask_value == "X":
            new_results = []
            for r in results:
                new_results.append([i for i in r] + ["0"])
                new_results.append([i for i in r] + ["1"])
                results = new_results
        else:
            raise Exception(mask_value)
    return [int("".join(r), 2) for r in results]


def run_tests():
    test_inputs = """
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 165:
        raise Exception(f"Test 1 did not past, got {result_1}")

    test_inputs = """
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 208:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(14)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
