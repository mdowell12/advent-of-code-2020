from solutions.get_inputs import read_inputs


class Cups2:

    def __init__(self, inputs, extra=None):
        numbers = [int(i) for i in inputs[0]]
        if extra:
            numbers += list(range(max(numbers) + 1, extra + 1))

        self.min = min(numbers)
        self.max = max(numbers)

        self.cups = {}
        for i, number in enumerate(numbers[:-1]):
            self.cups[number] = numbers[i+1]
        self.cups[numbers[-1]] = numbers[0]
        self.current_item = numbers[0]

    def take(self):
        # Get the next three cups
        cup1 = self.cups[self.current_item]
        cup2 = self.cups[cup1]
        cup3 = self.cups[cup2]

        # Remove them from the circle by linking the current cup
        # to the cup after the ones that were taken
        self.cups[self.current_item] = self.cups[cup3]

        return [cup1, cup2, cup3]

    def find_destination(self, taken_l):
        taken = set(taken_l)
        maybe_destination = self.current_item
        while True:
            maybe_destination = maybe_destination - 1
            if maybe_destination < self.min:
                maybe_destination = self.max
            if maybe_destination in taken:
                continue
            return maybe_destination

    def replace(self, taken, destination_value):
        item_after_destination = self.cups[destination_value]
        self.cups[destination_value] = taken[0]
        self.cups[taken[0]] = taken[1]
        self.cups[taken[1]] = taken[2]
        self.cups[taken[2]] = item_after_destination

    def next_turn(self):
        self.current_item = self.cups[self.current_item]

    def format(self):
        result = []
        item = self.cups[1]
        while item != 1:
            result.append(str(item))
            item = self.cups[item]
        return ''.join(result)

    def format2(self):
        return self.cups[1] * self.cups[self.cups[1]]

    def __repr__(self):
        return str(self.cups)


def run_1(inputs, num_turns):
    cups = Cups2(inputs)
    for _ in range(num_turns):
        taken = cups.take()
        destination = cups.find_destination(taken)
        cups.replace(taken, destination)
        cups.next_turn()

    return cups.format()


def run_2(inputs):
    cups = Cups2(inputs, 1_000_000)
    for i in range(10_000_000):
        if i % 100000 == 0:
            print(i)
        taken = cups.take()
        destination = cups.find_destination(taken)
        cups.replace(taken, destination)
        cups.next_turn()

    return cups.format2()


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

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
