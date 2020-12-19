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
    def generate_valid_messages(rule_number, rules):
        permutations = Rule.generate_permutations(rule_number, rules)
        print(permutations)
        combos = Rule.generate_combos(permutations[0])
        result = set([''])
        # import pdb; pdb.set_trace()
        for p in permutations[0]:
            possible_strings = []



            for s in result:
                new = s + ''.join(p)
                result.add(new)
        return result

    @staticmethod
    def generate_combos(permutations):
        if isinstance(permutations, str):
            return permutations
        # import pdb; pdb.set_trace()
        combos = []
        for p in permutations:

            thiscombo = Rule.generate_combos(p)
            import pdb; pdb.set_trace()
            if not combos:
                combos = [thiscombo]
            else:
                new_combos = []
                for c in combos:
                    for cc in thiscombo:
                        new_combos.append(c + cc)
                combos = new_combos
        return combos




    @staticmethod
    def generate_permutations(rule_number, rules):
        rule = rules[rule_number]

        if rule.is_root():
            return rule.possibilities[0][0]

        result = []
        for p in rule.possibilities:
            permutations = []
            for number in p:
                possibilities = Rule.generate_permutations(number, rules)
                # print(possibilities)
                permutations.append(possibilities)
            # print(permutations)
            result.append(permutations)
        return result


    def __repr__(self):
        return f'{self.key}: {self.possibilities}'


def run_1(inputs):
    rules, messages = parse_input(inputs)
    print(rules)
    print(messages)
    Rule.generate_valid_messages('0', rules)


def run_2(inputs):
    pass


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

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    # run_tests()
    print(Rule.generate_combos(['a']))
    print(Rule.generate_combos(['a', ['a', 'b']]))

    input = read_inputs(19)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
