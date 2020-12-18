from solutions.get_inputs import read_inputs


class Token(object):

    CHAR_MAP = {
        '+': 'PLUS',
        '*': 'MULT',
        '(': 'LPAREN',
        ')': 'RPAREN',
    }

    @staticmethod
    def tokenize(line):
        chars = [i for i in list(line) if i != ' ']
        tokens = []
        while chars:
            char = chars.pop(0)
            next = chars[0] if chars else ''
            if char == '(' or next == ')':
                tokens.append(Token(char))
                tokens.append(Token(chars.pop(0)))
            else:
                tokens.append(Token(char))
        return tokens

    def __init__(self, char):
        self.char = char
        self.token, self.value = self.lex_char(char)

    def lex_char(self, char):
        if char in self.CHAR_MAP:
            return self.CHAR_MAP[char], char
        return 'INT', int(char)

    def __repr__(self):
        return f'{self.value}'


class Evaluator(object):

    def __init__(self, tokens, part):
        self.tokens = [i for i in tokens]
        self.eval_block =  self.eval_block_1 if part == 1 else self.eval_block_2

    def eval(self):
        acc = self.eval_block()
        while self.tokens:
            operator = self.tokens.pop(0)
            right = self.eval_block()
            if operator.token == 'PLUS':
                acc += right
            elif operator.token == 'MULT':
                acc *= right
            else:
                raise Exception(operator)

        return acc

    def eval_block_1(self):
        next = self.tokens.pop(0)
        if next.token == 'INT':
            return next.value
        elif next.token == 'LPAREN':
            acc = self.eval_block()
            while self.tokens[0].token != 'RPAREN':
                operator = self.tokens.pop(0)
                right = self.eval_block()
                if operator.token == 'PLUS':
                    acc += right
                elif operator.token == 'MULT':
                    acc *= right
                else:
                    raise Exception(operator)
            # Pop the RPAREN
            self.tokens.pop(0)
            return acc
        else:
            raise Exception(next)

    def eval_block_2(self):
        next = self.tokens.pop(0)
        if next.token == 'LPAREN':
            acc = self.eval_block()
            while self.tokens[0].token != 'RPAREN':
                operator = self.tokens.pop(0)
                right = self.eval_block()
                if operator.token == 'PLUS':
                    acc += right
                elif operator.token == 'MULT':
                    acc *= right
                else:
                    raise Exception(operator)
            # Pop the RPAREN
            self.tokens.pop(0)
            if self.tokens and self.tokens[0].token == 'PLUS':
                self.tokens.pop(0)  # pop the PLUS
                right = self.eval_block()
                return acc + right
            else:
                return acc
        elif next.token == 'INT':
            if self.tokens and self.tokens[0].token == 'PLUS':
                left = next.value
                self.tokens.pop(0)  # pop the PLUS
                right = self.eval_block()
                return left + right
            else:
                return next.value

        else:
            raise Exception(next)


class Evaluator2(object):

    def __init__(self, tokens):
        self.tokens = [i for i in tokens]

    def eval(self):
        acc = self.eval_block()
        while self.tokens:
            operator = self.tokens.pop(0)
            right = self.eval_block()
            print(acc, operator, right)
            if operator.token == 'PLUS':
                acc += right
            elif operator.token == 'MULT':
                acc *= right
            else:
                raise Exception(operator)

        return acc

    def eval_block(self):
        next = self.tokens.pop(0)
        if next.token == 'LPAREN':
            acc = self.eval_block()
            while self.tokens[0].token != 'RPAREN':
                operator = self.tokens.pop(0)
                right = self.eval_block()
                if operator.token == 'PLUS':
                    acc += right
                elif operator.token == 'MULT':
                    acc *= right
                else:
                    raise Exception(operator)
            # Pop the RPAREN
            self.tokens.pop(0)
            if self.tokens and self.tokens[0].token == 'PLUS':
                self.tokens.pop(0)  # pop the PLUS
                right = self.eval_block()
                return acc + right
            else:
                return acc
        elif next.token == 'INT':
            if self.tokens and self.tokens[0].token == 'PLUS':
                left = next.value
                self.tokens.pop(0)  # pop the PLUS
                right = self.eval_block()
                return left + right
            else:
                return next.value

        else:
            raise Exception(next)


def run_1(inputs):
    return run(inputs, 1)


def run_2(inputs):
    return run(inputs, 2)


def run(inputs, part):
    result = 0
    for line in inputs:
        tokens = Token.tokenize(line.strip())
        val = Evaluator(tokens, part).eval()
        result += val
    return result


def run_tests():
    test_inputs = """
    2 + 3
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 5:
        raise Exception(f"Test 0 did not past, got {result_1}")

    test_inputs = """
    2 * 3
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 6:
        raise Exception(f"Test 0.1 did not past, got {result_1}")

    test_inputs = """
    2 * 3 + (4 * 5)
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 26:
        raise Exception(f"Test 1 did not past, got {result_1}")

    test_inputs = """
    5 + (8 * 3 + 9 + 3 * 4 * 3)
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 437:
        raise Exception(f"Test 1.2 did not past, got {result_1}")

    test_inputs = """
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 12240:
        raise Exception(f"Test 1.3 did not past, got {result_1}")

    test_inputs = """
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 13632:
        raise Exception(f"Test 1.4 did not past, got {result_1}")

    test_inputs = """
    2 * 3 + (4 * 5)
    2 * 3 + (4 * 5)
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 52:
        raise Exception(f"Test 1.5 did not past, got {result_1}")

    # Part 2
    test_inputs = """
    2 * 3 * 5 + 5
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 60:
        raise Exception(f"Test 0.2 did not past, got {result_2}")

    test_inputs = """
    (2 * 3) * (5 * 5) + 5
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 180:
        raise Exception(f"Test 0.2 did not past, got {result_2}")

    test_inputs = """
    2 * 3 + (4 * 5)
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 46:
        raise Exception(f"Test 2 did not past, got {result_2}")

    test_inputs = """
    5 + (8 * 3 + 9 + 3 * 4 * 3)
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 1445:
        raise Exception(f"Test 2.2 did not past, got {result_2}")

    test_inputs = """
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 669060:
        raise Exception(f"Test 2.3 did not past, got {result_2}")

    test_inputs = """
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 23340:
        raise Exception(f"Test 2.4 did not past, got {result_2}")

    test_inputs = """
    2 * 3 + (4 * 5)
    2 * 3 + (4 * 5)
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 92:
        raise Exception(f"Test 2.5 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(18)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
