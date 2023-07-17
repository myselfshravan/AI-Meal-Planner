import streamlit as st
import pandas as pd
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import random

ANTHROPIC_API_KEY = "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"
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

st.set_page_config(page_title="AI - Meal Planner", page_icon="🍴")
st.title("Knowledge based Meal Planner")

st.write(
    "This is a knowledge based meal planner that uses a persons information. The planner can be used to find a meal plan that satisfies the user's calorie and macronutrient requirements.")

food_items_breakfast = {
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

food_items_lunch = {
    "protein": {
        "grilled_chicken_breast": 165,
        "salmon_fillet": 206,
        "tofu": 144,
        "lean_beef": 176,
        "shrimp": 99
    },
    "whole_grains": {
        "brown_rice": 216,
        "quinoa": 222,
        "whole_wheat_pasta": 180,
        "barley": 270,
        "couscous": 176
    },
    "vegetables": {
        "leafy_greens": 10,
        "broccoli": 55,
        "cauliflower": 25,
        "carrots": 41,
        "bell_peppers": 31,
        "cucumbers": 16,
        "tomatoes": 18,
        "zucchini": 17
    },
    "legumes": {
        "chickpeas": 269,
        "lentils": 230,
        "black_beans": 227,
        "kidney_beans": 225,
        "edamame": 121
    },
    "healthy_fats": {
        "avocado": 234,
        "nuts": 160,
        "seeds": 160,
        "olive_oil": 119,
        "coconut_oil": 121
    },
    "dairy_or_dairy_alternatives": {
        "greek_yogurt": 130,
        "cottage_cheese": 206,
        "cheese": 113,
        "dairy-free_alternatives": 80
    },
    "additional_toppings_condiments": {
        "sliced_avocado": 50,
        "hummus": 27,
        "salsa": 20,
        "salad_dressings": 73,
        "herbs_and_spices": 0
    }
}

food_items_dinner = {
    "proteins": {
        "chicken_breast": 165,
        "salmon": 206,
        "beef_steak": 250,
        "tofu": 144,
        "shrimp": 84,
        "lentils": 116
    },
    "grains_and_starches": {
        "brown_rice": 216,
        "quinoa": 222,
        "sweet_potatoes": 180,
        "whole_wheat_pasta": 174,
        "couscous": 176,
        "barley": 193
    },
    "vegetables": {
        "broccoli": 55,
        "cauliflower": 25,
        "green_beans": 31,
        "asparagus": 27,
        "brussels_sprouts": 38,
        "carrots": 41,
        "zucchini": 17
    },
    "legumes": {
        "black_beans": 227,
        "chickpeas": 269,
        "kidney_beans": 333,
        "lentils": 353
    },
    "healthy_fats": {
        "avocado": 160,
        "olive_oil": 119,
        "nuts": 160,
        "seeds": 150
    },
    "dairy_or_dairy_alternatives": {
        "greek_yogurt": 59,
        "cheese": 113,
        "almond_milk": 40
    },
    "sauces_and_condiments": {
        "tomato_sauce": 32,
        "soy_sauce": 8,
        "balsamic_vinegar": 14,
        "mustard": 10,
        "salsa": 15,
        "guacamole": 50,
        "hummus": 27
    },
    "herbs_and_spices": {
        "basil": 22,
        "oregano": 5,
        "rosemary": 2,
        "thyme": 3,
        "cumin": 22,
        "paprika": 20,
        "garlic_powder": 9,
        "onion_powder": 7
    }
}


def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age + 5
    else:
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age - 161

    return bmr


def get_user_preferences():
    preferences = st.multiselect("Choose your food preferences:", list(food_items_breakfast.keys()))
    return preferences


def get_user_allergies():
    allergies = st.multiselect("Choose your food allergies:", list(food_items_breakfast.keys()))
    return allergies


st.write("Enter your personal information:")
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", step=1, value=20)
weight = st.number_input("Enter your weight (kg)", value=51)
height = st.number_input("Enter your height (cm)", value=169)
gender = st.radio("Choose your gender:", ["Male", "Female"])


def generate_items_list(target_calories, food_groups):
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


def generate_items_list_gh(target_calories, food_groups):
    calories = 0
    selected_items = []
    total_items = set()

    # Collect all available food items from the food_groups dictionary
    for foods in food_groups.values():
        total_items.update(foods.keys())

    # Create a list of food items sorted by calorie-to-value ratio in descending order
    sorted_items = sorted(total_items, key=lambda item: food_groups[item] / item, reverse=True)

    # Greedy selection using the sorted_items list
    for item in sorted_items:
        cals = food_groups[item]
        if calories + cals <= target_calories:
            selected_items.append(item)
            calories += cals

    return selected_items, calories


bmr = calculate_bmr(weight, height, age, gender)
st.subheader(f"Your daily intake needs to have: {bmr} calories")

pre_prompt_b = "I am giving you a list of items in my basket below and I want you to generate a meal for me using the items from the basket make sure to use most of the items and create a name for the dish and I will be giving you different items for breakfast in the basket and you need to generate a meal and the name of the meal by using all the items in each category that is breakfast, lunch, and dinner so this is the list for items for the breakfast meal: "

pre_prompt_l = "I am giving you a list of items in my basket below and I want you to generate a meal for me using the items from the basket make sure to use most of the items and create a name for the dish and I will be giving you different items for lunch in the basket and you need to generate a meal and the name of the meal by using all the items in each category that is breakfast, lunch, and dinner so this is the list for items for the lunch meal: "

pre_prompt_d = "I am giving you a list of items in my basket below and I want you to generate a meal for me using the items from the basket make sure to use most of the items and create a name for the dish and I will be giving you different items for dinner in the basket and you need to generate a meal and the name of the meal by using all the items in each category that is breakfast, lunch, and dinner so this is the list for items for the dinner meal: "

pre_breakfast = "For breakfast, we have a scrumptious dish called 'Sunrise Scramble'. It features fluffy scrambled eggs infused with earthy mushrooms and colorful bell peppers. This combination is guaranteed to kickstart your day with a burst of flavor and energy. This is just an example you can use your own creativity to generate based on the list provided."

pre_lunch = "Here the example but use your own creativity to generate based on the list provided : For lunch, we have a refreshing creation known as 'Tropical Yogurt Delight.' This mouthwatering salad combines creamy Greek yogurt with tangy oranges and crunchy nuts. Each bite will transport you to a tropical paradise, filling you with satisfaction and nourishment. This is just an example you can use your own creativity to generate based on the list provided. "

pre_dinner = "Here the example but use your own creativity to generate based on the list provided : Now, for the grand finale, let's dive into a dinner masterpiece called 'Stuffed Spinach Sensation.' Here, we take tender chicken breasts and fill them to the brim with a vibrant mixture of spinach and juicy tomatoes. The result is a tantalizing dish that will leave you craving more. This is just an example you can use your own creativity to generate based on the list provided."

end_text = "Remember, hydration is key to staying refreshed and energized throughout the day. So, keep a glass of water handy and sip it to your heart's content. Get ready to savor this extraordinary culinary experience and let your taste buds dance with joy. Enjoy your meals and have a fantastic day!"

example_response = f"This is just an example but use your creativity: You can start with, Hello {name}! I'm thrilled to be your meal planner for the day, and I've crafted a delightful and flavorful meal plan just for you. But fear not, this isn't your ordinary, run-of-the-mill meal plan. It's a culinary adventure designed to keep your taste buds excited while considering the calories you can intake. So, get ready!"

negative_prompt = "Do not include instruction to prepare the meal. I want only the name of the meal and the ingredients used in the meal. You your master chef cooking skills to generate the meal."

generate_items = st.button("Generate Meal Plan")
if generate_items:
    calories_breakfast = round((bmr * 0.5), 2)
    calories_lunch = round((bmr * (1 / 3)), 2)
    calories_dinner = round((bmr * (1 / 6)), 2)
    meal_items_morning, cal_m = generate_items_list(calories_breakfast, food_items_breakfast)
    meal_items_lunch, cal_l = generate_items_list(calories_lunch, food_items_lunch)
    meal_items_dinner, cal_d = generate_items_list(calories_dinner, food_items_dinner)
    st.header("Your Personalized Meal Plan")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Calories for Morning: " + str(calories_breakfast))
        st.dataframe(pd.DataFrame({"Morning": meal_items_morning}))
        st.write("Total Calories: " + str(cal_m))

    with col2:
        st.write("Calories for Lunch: " + str(calories_lunch))
        st.dataframe(pd.DataFrame({"Lunch": meal_items_lunch}))
        st.write("Total Calories: " + str(cal_l))

    with col3:
        st.write("Calories for Dinner: " + str(calories_dinner))
        st.dataframe(pd.DataFrame({"Dinner": meal_items_dinner}))
        st.write("Total Calories: " + str(cal_d))

    completion = anthropic.completions.create(
        model="claude-1",
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT}{pre_prompt_b}{str(meal_items_morning)}{example_response}{pre_breakfast}{negative_prompt}{AI_PROMPT}",
    )
    out_b = completion.completion
    st.write(out_b)
    completion = anthropic.completions.create(
        model="claude-1",
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT}{pre_prompt_l}{str(meal_items_lunch)}{pre_lunch}{negative_prompt}{AI_PROMPT}",
    )
    out_l = completion.completion
    st.write(out_l)
    completion = anthropic.completions.create(
        model="claude-1",
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT}{pre_prompt_d}{str(meal_items_dinner)}{pre_dinner}{negative_prompt}{AI_PROMPT}",
    )
    out_d = completion.completion
    st.write(out_d)
    st.write(end_text)

    st.write("Thank you for using our app! We hope you enjoyed it!")
