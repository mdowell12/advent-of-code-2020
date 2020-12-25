from solutions.get_inputs import read_inputs


def run_1(inputs):
    card_pub, door_pub = int(inputs[0]), int(inputs[1])
    card_loop = get_loop(card_pub)
    # door_loop = get_loop(door_pub)
    print(card_pub, door_pub, card_loop)
    return get_encryption_key(card_loop, door_pub)


def run_2(inputs):
    pass


def get_loop(public_key):
    subject_number = 7
    acc = 1
    step = 0
    while acc != public_key:
        acc *= subject_number
        acc = acc % 20201227
        step += 1
    return step


def get_encryption_key(loop_number, public_key):
    acc = 1
    for _ in range(loop_number):
        acc *= public_key
        acc = acc % 20201227
    return acc



def run_tests():
    result_1 = get_loop(5764801)
    if result_1 != 8:
        raise Exception(f"Test 1.2 did not past, got {result_1}")

    result_1 = get_loop(17807724)
    if result_1 != 11:
        raise Exception(f"Test 1.3 did not past, got {result_1}")

    test_inputs = """
    5764801
    17807724
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 14897079:
        raise Exception(f"Test 1 did not past, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(25)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
