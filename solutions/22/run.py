from solutions.get_inputs import read_inputs


def run_1(inputs):
    deck_1, deck_2 = parse_inputs(inputs)
    while deck_1 and deck_2:
        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)
        if card_1 > card_2:
            deck_1 += [card_1, card_2]
        elif card_1 < card_2:
            deck_2 += [card_2, card_1]
        else:
            raise Exception(card_1)

    return score(deck_1) if deck_1 else score(deck_2)


def score(deck):
    result = 0
    for i, val in enumerate(reversed(deck)):
        result += (i+1) * val
    return result


def run_2(inputs):
    deck_1, deck_2 = parse_inputs(inputs)
    deck_1, deck_2 = play(deck_1, deck_2)
    return score(deck_1) if deck_1 else score(deck_2)


def play(deck_1, deck_2, level=0):
    deck_1 = [i for i in deck_1]
    deck_2 = [i for i in deck_2]

    seen = set()

    while deck_1 and deck_2:
        turn_hash = hash_turn(deck_1, deck_2)

        if turn_hash in seen:
            break
        seen.add(turn_hash)

        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)

        if card_1 <= len(deck_1) and card_2 <= len(deck_2):
            recurse_deck_1, _ = play(deck_1[:card_1], deck_2[:card_2], level=level+1)
            if recurse_deck_1:
                player_1_wins = True
            else:
                player_1_wins = False
        else:
            if card_1 > card_2:
                player_1_wins = True
            else:
                player_1_wins = False

        if player_1_wins:
            deck_1 += [card_1, card_2]
        else:
            deck_2 += [card_2, card_1]

    return deck_1, deck_2


def hash_turn(deck_1, deck_2):
    return ','.join(str(i) for i in deck_1) + ':' + ','.join(str(i) for i in deck_2)


def parse_inputs(inputs):
    inputs = [i for i in inputs]
    deck_1, deck_2 = [], []
    deck = deck_1
    while inputs:
        line = inputs.pop(0).strip()
        if 'Player 2' in line:
            deck = deck_2
        elif line.isdigit():
            deck.append(int(line))

    return deck_1, deck_2


def run_tests():
    test_inputs = """
    Player 1:
    9
    2
    6
    3
    1

    Player 2:
    5
    8
    4
    7
    10
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 306:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 291:
        raise Exception(f"Test 2 did not past, got {result_2}")

    test_inputs = """
    Player 1:
    43
    19

    Player 2:
    2
    29
    14
    """.strip().split('\n')
    # Just make sure it doesn't infinitely loop
    run_2(test_inputs)

    print("tests passed")

if __name__ == "__main__":
    run_tests()

    input = read_inputs(22)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
