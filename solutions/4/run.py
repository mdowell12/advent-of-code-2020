from solutions.get_inputs import read_inputs


def rule_hgt(x):
    if len(x) < 3:
        return False
    suffix = x[-2:]
    prefix = x[:-2]
    if not prefix.isnumeric():
        return False
    if suffix == 'cm':
        return int(prefix) >= 150 and int(prefix) <= 193
    elif suffix == 'in':
        return int(prefix) >= 59 and int(prefix) <= 76
    else:
        return False


def rule_hcl(x):
    if not x or not x[0] == "#":
        return False
    return all(i.isnumeric() or i.isalpha() for i in x[1:])


FIELD_RULES = {
    'byr': lambda x: len(x) == 4 and x.isnumeric() and int(x) >= 1920 and int(x) <= 2002,
    'iyr': lambda x: len(x) == 4 and x.isnumeric() and int(x) >= 2010 and int(x) <= 2020,
    'eyr': lambda x: len(x) == 4 and x.isnumeric() and int(x) >= 2020 and int(x) <= 2030,
    'hgt': rule_hgt,
    'hcl': rule_hcl,
    'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': lambda x: len(x) == 9 and all(s.isnumeric() for s in x),
}

def run_1(inputs):
    passports = parse_passports(inputs)
    return sum(1 if is_valid_1(p) else 0 for p in passports)


def run_2(inputs):
    passports = parse_passports(inputs)
    return sum(1 if is_valid_2(p) else 0 for p in passports)


def is_valid_1(passport):
    for field in FIELD_RULES:
        if field not in passport:
            return False
    return True


def is_valid_2(passport):
    for field, rule in FIELD_RULES.items():
        if field not in passport:
            return False
        if not rule(passport[field]):
            return False

    return True


def parse_passports(lines):
    passports = []
    acc = []
    for line in lines:
        cleaned = line.strip()
        if len(cleaned) > 0:
            acc.append(cleaned)
        else:
            passports.append(parse_single_passport(acc))
            acc = []
    if acc:
        passports.append(parse_single_passport(acc))
    return passports


def parse_single_passport(lines):
    passport = {}
    for line in lines:
        parts = line.split(' ')
        for part in parts:
            k, v = part.split(':', 1)
            passport[k] = v
    return passport


def run_tests():
    test_inputs = """
    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 2:
        raise Exception(f"Test 1 did not past, got {result_1}")

    test_inputs_2 = """
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007

    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    """.strip().split('\n')

    result_2 = run_2(test_inputs_2)
    if result_2 != 4:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(4)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
