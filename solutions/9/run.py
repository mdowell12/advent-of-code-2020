from solutions.get_inputs import read_inputs


class Stream(object):

    def __init__(self, inputs, preamble_length):
        self.items = [int(i) for i in inputs]
        self.preamble_length = preamble_length

    def first_invalid(self):
        for i in range(self.preamble_length, len(self.items)):
            if not self.is_valid_item(i):
                return i, self.items[i]

        # All valid
        return None, None

    def is_valid_item(self, position):
        predecessors = [self.items[i] for i in range(position - self.preamble_length, position)]
        current_item = self.items[position]
        for i, predecessor in enumerate(predecessors):
            other_predecessors = {item for j, item in enumerate(predecessors) if j != i}
            if current_item - predecessor in other_predecessors:
                return True
        return False

    def encryption_weakness(self):
        position_of_first_invalid, first_invalid = self.first_invalid()
        left = 0
        right = 1
        for left in range(position_of_first_invalid):
            for right in range(left + 1, position_of_first_invalid):
                items_to_try = self.items[left:right+1]
                if sum(items_to_try) == first_invalid:
                    return min(items_to_try) + max(items_to_try)
        return None


def run_1(inputs, preamble_length):
    s = Stream(inputs, preamble_length)
    _, val = s.first_invalid()
    return val


def run_2(inputs, preamble_length):
    s = Stream(inputs, preamble_length)
    return s.encryption_weakness()


def run_tests():
    test_inputs = """
    35
    20
    15
    25
    47
    40
    62
    55
    65
    95
    102
    117
    150
    182
    127
    219
    299
    277
    309
    576
    """.strip().split('\n')

    result_1 = run_1(test_inputs, 5)
    if result_1 != 127:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs, 5)
    if result_2 != 62:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(9)

    result_1 = run_1(input, 25)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input, 25)
    print(f"Finished 2 with result {result_2}")
