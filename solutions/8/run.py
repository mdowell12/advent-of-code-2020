from solutions.get_inputs import read_inputs


class AlreadyExecutedException(Exception):
    pass


class Program(object):

    def __init__(self, lines):
        self.acc = 0
        self.current_line = 0
        self.lines = {i: line.strip() for i, line in enumerate(lines)}
        self.lines_executed = set()

    def run(self):
        while True:
            if self.should_exit():
                return self.value()
            if self.already_executed():
                raise AlreadyExecutedException()
            self.execute_line()

    def execute_line(self):
        command, value = self.lines[self.current_line].split(' ')
        self.lines_executed.add(self.current_line)
        if command == 'nop':
            self.current_line += 1
        elif command == 'acc':
            self.acc += self._parse_int_value(value)
            self.current_line += 1
        elif command == 'jmp':
            self.current_line += self._parse_int_value(value)


    def already_executed(self):
        return self.current_line in self.lines_executed

    def value(self):
        return self.acc

    def should_exit(self):
        return self.current_line == len(self.lines)

    @staticmethod
    def _parse_int_value(value):
        is_positive = value[0] == '+'
        base = int(value[1:])
        return base if is_positive else -1 * base


def run_1(inputs):
    p = Program(inputs)
    try:
        p.run()
    except AlreadyExecutedException:
        # Expected
        return p.value()


def run_2(inputs):
    inputs_warped = [i for i in inputs]
    pos = 0
    while True:
        p = Program(inputs_warped)
        try:
            return p.run()
        except AlreadyExecutedException:
            pass
        inputs_warped = [val if i != pos else try_swap(val) for i, val in enumerate(inputs)]
        pos += 1


def try_swap(value):
    if 'nop' in value:
        return value.replace('nop', 'jmp')
    elif 'jmp' in value:
        return value.replace('jmp', 'nop')
    else:
        return value


def run_tests():
    test_inputs = """
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 5:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 8:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(8)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
