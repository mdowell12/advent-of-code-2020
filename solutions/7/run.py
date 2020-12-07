from solutions.get_inputs import read_inputs


def run_1(inputs):
    rules = build_rules(inputs)
    my_color = 'shiny gold'
    can_contain_mine = colors_containing(my_color, rules)
    to_check = set(i for i in can_contain_mine)
    while to_check:
        next_to_check = set()
        for color in to_check:
            can_contain_color = colors_containing(color, rules)
            can_contain_mine = can_contain_mine.union(can_contain_color)
            next_to_check = next_to_check.union(can_contain_color)
        to_check = next_to_check
    return len(can_contain_mine)


def run_2(inputs):
    rules = build_rules(inputs)
    queue = [color for color in rules['shiny gold']]
    total_bags = 0
    while queue:
        total_bags += len(queue)
        next_bags = [rules[color] for color in queue]
        queue = [color for color_list in next_bags for color in color_list]

    return total_bags


def colors_containing(other_color, rules):
    return set(r for r in rules.keys() if other_color in rules[r])


def build_rules(inputs):
    result = {}
    for line in inputs:
        k, v = parse_rule(line)
        result[k] = v
    return result


def parse_rule(line):
    first, second = line.split('contain', 1)
    color = parse_color(first)
    contains = parse_contains(second)
    return color, contains


def parse_color(first):
    return first.replace('bags', '').strip()


def parse_contains(second):
    if 'no other bags' in second:
        return []
    result = []
    parts = second.replace('.', '').split(',')
    for part in parts:
        cleaned = part.replace('bags', '').replace('bag', '').strip()
        num, color = cleaned.split(' ', 1)
        colors = [color for _ in range(int(num))]
        result += colors
    return result


def run_tests():
    test_inputs = """
    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 4:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 32:
        raise Exception(f"Test 2 did not past, got {result_2}")

    test_inputs2 = """
    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.
    """.strip().split('\n')

    result_3 = run_2(test_inputs2)
    if result_3 != 126:
        raise Exception(f"Test 3 did not past, got {result_3}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(7)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
