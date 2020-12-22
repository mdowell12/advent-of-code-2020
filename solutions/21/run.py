from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    foods = [parse_line(l) for l in inputs]

    allergen_to_foods, ingredient_to_allergens, cannot_be_allergen = get_maps(foods)

    result = 0
    for ingredient in cannot_be_allergen:
        result += len([f for f, _ in foods if ingredient in f])

    return result


def get_maps(foods):
    allergen_to_foods = defaultdict(list)
    ingredient_to_allergens = defaultdict(set)

    for ingredients, allergens in foods:
        for allergen in allergens:
            allergen_to_foods[allergen].append(ingredients)
        for ingredient in ingredients:
            ingredient_to_allergens[ingredient] = ingredient_to_allergens[ingredient].union(allergens)

    cannot_be_allergen = set()
    for ingredient, allergens in ingredient_to_allergens.items():
        if all(ingredient_cannot_be_this_allergen(allergen, ingredient, allergen_to_foods) for allergen in allergens):
            cannot_be_allergen.add(ingredient)

    return allergen_to_foods, ingredient_to_allergens, cannot_be_allergen


def ingredient_cannot_be_this_allergen(allergen, ingredient, allergen_to_foods):
    foods_with_allergen = allergen_to_foods[allergen]
    if any(ingredient not in food for food in foods_with_allergen):
        return True
    return False


def run_2(inputs):
    foods = [parse_line(l) for l in inputs]
    _, ingredient_to_allergens, cannot_be_allergen = get_maps(foods)

    # Remove ingredients that cannot be an allergen
    for ingredient in cannot_be_allergen:
        del ingredient_to_allergens[ingredient]
        foods = remove_ingredient_from_foods(foods, ingredient)

    # Consolidate into one row per food
    unique_foods = []
    for food in foods:
        matching = [f for f in unique_foods if f[0] == food[0]]
        if matching:
            [matching[0][-1].add(i) for i in food[-1]]
        else:
            unique_foods.append(food)
    foods = unique_foods

    # Solve
    decisions = {ingredient: None for ingredient in ingredient_to_allergens.keys()}
    print("\n".join(sorted(str(i) for i in foods)))
    while (any(d is None for d in decisions.values())):
        variables = [f for f in foods if len(f[0]) == len(f[1])]

        for ingredients, allergens in foods:
            for v_ingredients, v_allergens in variables:
                allergens_without = allergens - v_allergens
                ingredients_without = ingredients - v_ingredients
                if len(allergens_without) == 1 and len(ingredients_without) == 1:
                    decisions[next(iter(ingredients_without))] = next(iter(allergens_without))

        for ingredient, allergen in decisions.items():
            if allergen is not None:
                foods = remove_ingredient_from_foods(foods, ingredient)
                foods = remove_allergen_from_foods(foods, allergen)

    # Format result
    rev = {v: k for k,v  in decisions.items()}
    return ",".join([rev[k] for k in sorted(decisions.values())])


def remove_ingredient_from_foods(foods, ingredient):
    new_foods = []
    for ingredients, allergens in foods:
        new_ingredients = ingredients - {ingredient,}
        new_foods.append((new_ingredients, allergens))
    return new_foods


def remove_allergen_from_foods(foods, allergen):
    new_foods = []
    for ingredients, allergens in foods:
        new_allergens = allergens - {allergen,}
        new_foods.append((ingredients, new_allergens))
    return new_foods


def parse_line(line):
    left, right = line.split('(contains')
    ingredients = set(left.strip().split(' '))
    allergens = set(right.strip().replace(')', '').replace(' ', '').split(','))
    return ingredients, allergens

def run_tests():
    test_inputs = """
    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 5:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 'mxmxvkd,sqjhc,fvjkl':
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(21)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
