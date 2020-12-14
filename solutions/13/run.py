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
    # Assume first one isn't an x
    # first = int(buses[0])
    # t = first
    # while True:
    #     # print(t)
    #     if is_valid_time(t, buses):
    #         return t
    #     t += first
    biggest = max(i for i in buses if i != 'x')
    i_biggest = buses.index(biggest)
    t = biggest * (int(100000000000000 / biggest) + 1)
    while True:
        if t % 100000 == 0:
            print(t)
        if is_valid_time(t, i_biggest, buses):
            return t - i_biggest
        t += biggest

# def is_valid_time(t, buses):
#     # if t >= 1068774:
#     #     import pdb; pdb.set_trace()
#     for i, bus in enumerate(buses):
#         if bus != "x" and (t + i) % int(bus) != 0:
#             return False
#     return True
def is_valid_time(t, i_biggest, buses):
    # if t >= 1068774:
    # import pdb; pdb.set_trace()
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
    # run_tests()

    input = read_inputs(13)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")
    # 103665810300000 too low
    # 1182922135469659 - 1 is upper bound b/c 1182922135469659 is LCD and that means cycle restarts
    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
    """
    <function diophantine at 0x1073c51f0>
>>> diophantine(17*a+41*b+643*c+23*d+13*e+29*f+433*g+37*h+19*i-9*t-294)
{(t_0, t_0 + t_1, t_0 + t_1 + t_2, t_0 + t_1 + t_2 + t_3, t_0 + t_1 + t_2 + t_3 + t_4, t_0 + t_1 + t_2 + t_3 + t_4 + t_5, t_0 + t_1 + t_2 + t_3 + t_4 + t_5 + t_6, t_0 + t_1 + t_2 + t_3 + t_4 + t_5 + t_6 + t_7, -1227*t_0 - 1210*t_1 - 1169*t_2 - 526*t_3 - 503*t_4 - 490*t_5 - 461*t_6 - 28*t_7 + 9*t_8 + 294, -2453*t_0 - 2419*t_1 - 2337*t_2 - 1051*t_3 - 1005*t_4 - 979*t_5 - 921*t_6 - 55*t_7 + 19*t_8 + 588)}
>>> res = diophantine(17*a+41*b+643*c+23*d+13*e+29*f+433*g+37*h+19*i-9*t-294)
>>> len(res)
1
>>> len(list(res)[0])
10
>>> list(res)[0]
(t_0, t_0 + t_1, t_0 + t_1 + t_2, t_0 + t_1 + t_2 + t_3, t_0 + t_1 + t_2 + t_3 + t_4, t_0 + t_1 + t_2 + t_3 + t_4 + t_5, t_0 + t_1 + t_2 + t_3 + t_4 + t_5 + t_6, t_0 + t_1 + t_2 + t_3 + t_4 + t_5 + t_6 + t_7, -1227*t_0 - 1210*t_1 - 1169*t_2 - 526*t_3 - 503*t_4 - 490*t_5 - 461*t_6 - 28*t_7 + 9*t_8 + 294, -2453*t_0 - 2419*t_1 - 2337*t_2 - 1051*t_3 - 1005*t_4 - 979*t_5 - 921*t_6 - 55*t_7 + 19*t_8 + 588)
>>> exit()
"""
