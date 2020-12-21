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

    allergen_to_foods, ingredient_to_allergens, cannot_be_allergen = get_maps(foods)

    for ingredient in cannot_be_allergen:
        # if allergen in allergen_to_foods:
            # del allergen_to_foods[allergen]
        del ingredient_to_allergens[ingredient]
        foods = remove_ingredient_from_foods(foods, ingredient)
        # ingredients = [i for i in ingredient_to_allergens.keys()]
        # for ingredient in ingredient_to_allergens:
        #     ingredient_to_allergens[ingredient] = ingredient_to_allergens[ingredient] - cannot_be_allergen

    """
    mxmxvkd sqjhc (contains dairy, fish)
    fvjkl mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd (contains fish)
    """

    decisions = {ingredient: None for ingredient in ingredient_to_allergens.keys()}
    import pdb; pdb.set_trace()
    while (any(d is None for d in decisions.values())):

        foods = remove_inelligibles(foods, ingredient_to_allergens)

        # for ingredient, allergens in ingredient_to_allergens.items():
        for ingredients, allergens in foods:
            if len(ingredients) == 1 and len(allergens) == 1:
                decisions[next(iter(ingredients))] = next(iter(allergens))

        print(decisions)


def remove_ingredient_from_foods(foods, ingredient):
    new_foods = []
    for ingredients, allergens in foods:
        new_ingredients = ingredients - {ingredient,}
        new_foods.append((new_ingredients, allergens))
    return new_foods


def remove_inelligibles(foods, ingredient_to_allergens):
    # new_foods = []
    # import pdb; pdb.set_trace()
    variable_foods = [f for f in foods if len(f[0]) == len(f[1])]
    ingredients_from_variable_foods = set(*[i for i, _ in variable_foods])

    other_foods = [f for f in foods if len(f[0]) != len(f[1])]

    # for ingredients, allergens in other_foods:
    #     new_ingredients = ingredients - ingredients_from_variable_foods
    #     new_food = (ingredients, allergen)
    #     new_foods.append(new_food)
    for ingredient in ingredients_from_variable_foods:
        other_foods = remove_ingredient_from_foods(other_foods, ingredient)

    return other_foods + variable_foods



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
