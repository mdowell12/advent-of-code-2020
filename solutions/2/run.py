from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    valid = 0
    for line in inputs:
        range = parse_input_range(line)
        letter = parse_letter(line)
        password = parse_password(line)
        if is_valid_password_1(password, letter, range):
            valid += 1

    return valid


def run_2(inputs):
    valid = 0
    for line in inputs:
        range = parse_input_range(line)
        letter = parse_letter(line)
        password = parse_password(line)
        if is_valid_password_2(password, letter, range):
            valid += 1

    return valid


def is_valid_password_1(password, letter, range):
    counts = defaultdict(lambda: 0)
    for l in password:
        counts[l] += 1
    return counts[letter] >= range[0] and counts[letter] <= range[1]


def is_valid_password_2(password, letter, range):
    first = password[range[0] - 1] == letter
    second = password[range[1] - 1] == letter
    return first != second


def parse_input_range(line):
    return [int(i) for i in line.strip().split(' ')[0].split('-')]


def parse_letter(line):
    return line.strip().split(' ')[1].replace(':', '')


def parse_password(line):
    return line.strip().split(' ')[2].strip()


def run_tests():
    test_inputs = """
    1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc""".strip().split('\n')

    result_1 = run_1([i.strip() for i in test_inputs])
    if result_1 != 2:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2([i.strip() for i in test_inputs])
    if result_2 != 1:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(2)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
