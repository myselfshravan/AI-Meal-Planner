import random

food_item_morning = {
    "protein": {
        "eggs": 78,
        "greek_yogurt": 130,
        "cottage_cheese": 206,
        "turkey_slices": 104,
        "smoked_salmon": 117
    },

    "whole_grains": {
        "whole_wheat_bread": 79,
        "oatmeal": 150,
        "quinoa": 222,
        "whole_grain_cereal": 120,
        "granola": 494
    },
    "fruits": {
        "berries": 50,
        "bananas": 96,
        "apples": 52,
        "oranges": 62,
        "grapefruit": 52,
        "melon_slices": 30
    },
    "vegetables": {
        "spinach": 7,
        "tomatoes": 18,
        "avocado": 160,
        "bell_peppers": 25,
        "mushrooms": 15
    },
    "healthy_fats": {
        "nut_butter": 94,
        "nuts": 163,
        "chia_seeds": 58,
        "flaxseeds": 55,
        "avocado_slices": 50
    },
    "dairy": {
        "milk": 103,
        "cheese": 113,
        "yogurt": 150,
        "dairy-free_alternatives": 80
    },
    "other": {
        "honey": 64,
        "maple_syrup": 52,
        "coffee": 2,
        "jam": 49,
        "peanut_butter": 188,
        "cocoa_powder": 12
    }
}


def select_breakfast(target_calories, food_groups):
    calories = 0
    selected_items = []
    total_items = set()
    for foods in food_groups.values():
        total_items.update(foods.keys())

    while abs(calories - target_calories) >= 10 and len(selected_items) < len(total_items):
        group = random.choice(list(food_groups.keys()))
        foods = food_groups[group]
        item = random.choice(list(foods.keys()))

        if item not in selected_items:
            cals = foods[item]
            if calories + cals <= target_calories:
                selected_items.append(item)
                calories += cals

    return selected_items, calories


# Example usage
target_cals = 500
itms, cal = select_breakfast(target_cals, food_item_morning)
print(itms)
print(f"Calories: {cal}")
# print(breakfast)
