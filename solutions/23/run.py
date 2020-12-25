from solutions.get_inputs import read_inputs


class Cups(object):

    def __init__(self, inputs, extra=None):
        self.cups = [int(i) for i in inputs[0].strip()]
        self.min = min(self.cups)
        if extra:
            self.cups += [i for i in range(max(self.cups) + 1, extra + 1)]
        self.max = max(self.cups)

    def take(self, n):
        return [self.cups.pop(1) for _ in range(n)]

    def find_destination(self, taken_l):
        taken = set(taken_l)
        cur_val = self.cups[0]
        maybe_destination = cur_val
        while True:
            maybe_destination = maybe_destination - 1
            if maybe_destination < self.min:
                maybe_destination = self.max
            if maybe_destination in taken:
                continue
            return self.cups.index(maybe_destination)

    def replace(self, taken, destination_i):
        self.cups = self.cups[:destination_i+1] + taken + self.cups[destination_i+1:]

    def next_turn(self):
        self.cups = self.cups[1:] + [self.cups[0]]

    def format(self):
        s = ''.join(str(i) for i in self.cups)
        parts = s.split('1', 2)
        return parts[1] + parts[0]

    def __repr__(self):
        return str([c if i != 0 else f'({c})' for i, c in enumerate(self.cups)])


def run_1(inputs, num_turns):
    cups = Cups(inputs)
    for i in range(num_turns):
        taken = cups.take(3)
        destination = cups.find_destination(taken)
        cups.replace(taken, destination)
        # print('turn:', i, 'cups:', cups)
        cups.next_turn()

    return cups.format()



def run_2(inputs):
    cups = Cups(inputs, 1_000_000)
    # print(cups.min, cups.max, len(cups.cups), len(set(cups.cups)))
    for i in range(10_000_000):
        if i * 1_000 == 0:
            print(i)
        taken = cups.take(3)
        destination = cups.find_destination(taken)
        cups.replace(taken, destination)
        cups.next_turn()

def run_tests():
    test_inputs = """
    389125467
    """.strip().split('\n')

    result_1 = run_1(test_inputs, 10)
    if result_1 != '92658374':
        raise Exception(f"Test 0 did not past, got {result_1}")

    result_1 = run_1(test_inputs, 100)
    if result_1 != '67384529':
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 149245887792:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(23)

    result_1 = run_1(input, 100)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
