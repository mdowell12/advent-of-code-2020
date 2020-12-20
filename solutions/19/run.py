from solutions.get_inputs import read_inputs


class Rule(object):

    LETTERS = set(["a", "b"])

    def __init__(self, line):
        self.key, self.possibilities = self._parse(line)

    def _parse(self, line):
        key, remaining = line.strip().split(':')
        possibilities = [[i.replace('"', '') for i in s.strip().split(' ')] for s in remaining.strip().split(' | ')]
        return key, possibilities

    def is_root(self):
        return self.possibilities[0][0] in self.LETTERS

    @staticmethod
    def get_strings_for_rule(rule_number, rules):

        rule = rules[rule_number]
        if rule.is_root():
            return rule.possibilities[0]

        result = []
        for possibility in rule.possibilities:
            strings = [Rule.get_strings_for_rule(r, rules) for r in possibility]
            for i in strings[0]:
                hack = strings[1] if len(strings) > 1 else ['']
                for j in hack:
                    this = i+j
                    result.append(this)
        return result

    def __repr__(self):
        return f'{self.key}: {self.possibilities}'


def run_1(inputs):
    rules, messages = parse_input(inputs)

    possibles = [Rule.get_strings_for_rule(r, rules) for r in rules['0'].possibilities[0]]

    acc = ['']
    for possible in possibles:
        news = []
        for a in acc:
            for s in possible:
                news.append(a + s)
        acc = news

    valid_messages = set(acc)
    return len([m for m in messages if m in valid_messages])


def run_2(inputs):
    rules, messages = parse_input(inputs)
    # Rule 0 is 8 11, with the following substitutes:
    # rules['8'] = Rule('8: 42 | 42 8')
    # rules['11'] = Rule('11: 42 31 | 42 11 31')
    # So all valid messages are a combo of strings valid for rule 42 or 31
    r31 = set(Rule.get_strings_for_rule('31',rules))
    r42 = set(Rule.get_strings_for_rule('42',rules))

    valid = []
    for message in messages:
        # It happens that all valid messages for rule 42 or 31 are of the same length
        # so chunk the messages up into chunks of that length
        n = min(len(i) for i in r31)
        chunks = [message[i:i+n] for i in range(0, len(message), n)]
        # Check if the sequence of chunks is a valid ordering of rule 42 and 31 strings
        if chunks_valid(chunks, r42, r31):
            valid.append(message)

    return len(valid)


def chunks_valid(chunks, r42, r31):
    """
    For a sequence of equal sized substrings of a message, check if they
    follow a valid pattern for rule 0.
    """
    if not chunks[0] in r42:
        return False
    if not chunks[1] in r42:
        return False
    if not chunks[-1] in r31:
        return False
    is_42 = True
    test = []
    for chunk in chunks:
        if not is_42:
            if chunk not in r31:
                return False
            else:
                test.append('31')
        else:
            if chunk not in r42:
                is_42 = False
                if chunk not in r31:
                    return False
                else:
                    test.append('31')
            else:
                test.append('42')

    if len([i for i in test if i == '31']) >= len([i for i in test if i == '42']):
        return False

    print(''.join(chunks), len(''.join(chunks)), len(''.join(chunks))/len(chunks[0]), ' '.join(test))
    return True


def parse_input(inputs):
    rules = [Rule(l) for l in inputs if ':' in l]
    messages = [i.strip() for i in inputs if i and ':' not in i]
    return {r.key: r for r in rules}, messages


def run_tests():
    test_inputs = """
    0: 4 1 5
    1: 2 3 | 3 2
    2: 4 4 | 5 5
    3: 4 5 | 5 4
    4: "a"
    5: "b"

    ababbb
    bababa
    abbbab
    aaabbb
    aaaabbb
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 2:
        raise Exception(f"Test 1 did not past, got {result_1}")

    test_inputs = """
    42: 9 14 | 10 1
    9: 14 27 | 1 26
    10: 23 14 | 28 1
    1: "a"
    11: 42 31
    5: 1 14 | 15 1
    19: 14 1 | 14 14
    12: 24 14 | 19 1
    16: 15 1 | 14 14
    31: 14 17 | 1 13
    6: 14 14 | 1 14
    2: 1 24 | 14 4
    0: 8 11
    13: 14 3 | 1 12
    15: 1 | 14
    17: 14 2 | 1 7
    23: 25 1 | 22 14
    28: 16 1
    4: 1 1
    20: 14 14 | 1 15
    3: 5 14 | 16 1
    27: 1 6 | 14 18
    14: "b"
    21: 14 1 | 1 14
    25: 1 1 | 1 14
    22: 14 14
    8: 42
    26: 14 22 | 1 20
    18: 15 15
    7: 14 5 | 1 21
    24: 14 1

    abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaaaabbaaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    babaaabbbaaabaababbaabababaaab
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 12:
        raise Exception(f"Test 2 did not past, got {result_2}")
    print("tests passed")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(19)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")
    # not 370
    # 365 too high
    # 355 too high
    # 348 is incorrect
    # 343 is incorrect
    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
