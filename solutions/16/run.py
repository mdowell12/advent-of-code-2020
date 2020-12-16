from solutions.get_inputs import read_inputs


def run_1(inputs):
    rules, my_ticket, other_tickets = parse_input(inputs)
    result = 0
    for ticket in other_tickets:
        invalid = invalid_values(ticket, rules)
        result += sum(invalid)
    return result


def run_2(inputs):
    parsed = parse_my_ticket(inputs)
    result = 1
    for k, v in parsed.items():
        if k.startswith('departure'):
            result *= v
    return result


def parse_my_ticket(inputs):
    rules, my_ticket, other_tickets = parse_input(inputs)
    if invalid_values(my_ticket, rules):
        raise Exception()

    valid_tickets = [t for t in other_tickets if not invalid_values(t, rules)]

    # Find all possible positions for a rule
    possible_rules_for_positions = {}
    for i in range(len(my_ticket)):
        rules_for_position = get_rules_for_position(i, valid_tickets, rules)
        possible_rules_for_positions[i] = rules_for_position

    # Assign rules to positions
    position_to_rule = {}
    while any(i not in position_to_rule for i in possible_rules_for_positions):
        one_possibile = [i for i, names in possible_rules_for_positions.items() if len(names) == 1]
        for i in one_possibile:
            name = possible_rules_for_positions[i][0]
            position_to_rule[i] = name
            del possible_rules_for_positions[i]
            for names in possible_rules_for_positions.values():
                names.remove(name)

    print(position_to_rule)
    return {name: my_ticket[i] for i, name in position_to_rule.items()}


def get_rules_for_position(i, valid_tickets, rules):
    values_for_position = [ticket[i] for ticket in valid_tickets]
    result = []
    for name, criteria in rules.items():
        if all(is_valid_for_criteria(v, criteria) for v in values_for_position):
            result.append(name)
    return result


def invalid_values(ticket, rules):
    """
    Can be used to test if ticket is invalid too.
    """
    result = []
    for value in ticket:
        if not is_valid(value, rules):
            result.append(value)
    return result


def is_valid(value, rules):
    for rule in rules.values():
        if is_valid_for_criteria(value, rule):
            return True
    return False


def is_valid_for_criteria(value, criteria):
    return any(value >= c[0] and value <= c[1] for c in criteria)


def parse_input(inputs):
    rules = {}
    my_ticket = None
    other_tickets = []

    while inputs:
        line = inputs.pop(0)
        if not line:
            pass
        elif 'your ticket' in line:
            line = inputs.pop(0)
            my_ticket = [int(i) for i in line.split(',')]
        elif 'nearby' in line:
            pass
        elif ':' in line:
            k, v = parse_rule(line)
            rules[k] = v
        else:
            other_tickets.append([int(i) for i in line.split(',')])

    return rules, my_ticket, other_tickets


def parse_rule(line):
    k, rule_text = line.strip().split(':')
    rules = []
    for range_text in rule_text.split(' or '):
        left, right = range_text.split('-')
        rules.append([int(left), int(right)])
    return k, rules


def run_tests():
    test_inputs = """
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 71:
        raise Exception(f"Test 1 did not past, got {result_1}")

    test_inputs = """
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9
    """.strip().split('\n')

    result_2 = parse_my_ticket(test_inputs)
    if result_2 != {'class': 12, 'row': 11, 'seat': 13}:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(16)
    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    input = read_inputs(16)
    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
