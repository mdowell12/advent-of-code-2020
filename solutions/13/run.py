from solutions.get_inputs import read_inputs


def run_1(inputs):
    wait_until = int(inputs[0].strip())
    buses = [int(i) for i in inputs[1].strip().split(',') if i != 'x']
    quotients = {int(wait_until / bus): bus for bus in buses}
    values_passed_time = {(k+1)*v: v for k, v in quotients.items()}
    earliest = min(values_passed_time.keys())
    bus_id = values_passed_time[earliest]

    return (earliest - wait_until) * bus_id


def run_2(inputs):
    buses = [int(i) if i != 'x' else i for i in inputs[1].strip().split(',')]
    current_guess = buses[0]
    current_inc = current_guess
    for i, bus in enumerate(buses[:-1]):
        if buses[i+1] == 'x':
            continue
        while (current_guess + i + 1) % buses[i+1] != 0:
            current_guess += current_inc

        current_inc = current_inc * buses[i+1]
    return current_guess


def is_valid_time(t, i_biggest, buses):
    for i, bus in enumerate(buses):
        if bus == "x":
            continue
        diff = i - i_biggest
        time_for_this_bus = t + diff
        if time_for_this_bus % int(bus) != 0:
            return False
    return True


def run_tests():
    test_inputs = """
    939
    7,13,x,x,59,x,31,19
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 295:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 1068781:
        raise Exception(f"Test 2 did not pass, got {result_2}")

    result_2 = run_2([0, "17,x,13,19"])
    if result_2 != 3417:
        raise Exception(f"Test 2.1 did not pass, got {result_2}")

    result_2 = run_2([0, "67,7,59,61"])
    if result_2 != 754018:
        raise Exception(f"Test 2.2 did not pass, got {result_2}")

    result_2 = run_2([0, "67,x,7,59,61"])
    if result_2 != 779210:
        raise Exception(f"Test 2.3 did not pass, got {result_2}")

    result_2 = run_2([0, "67,7,x,59,61"])
    if result_2 != 1261476:
        raise Exception(f"Test 2.4 did not pass, got {result_2}")

    result_2 = run_2([0, "1789,37,47,1889"])
    if result_2 != 1202161486:
        raise Exception(f"Test 2.5 did not pass, got {result_2}")

    print("Tests passed")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(13)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
