# Meal Planner App

This project is a meal planning app that generates personalized meal plans based on a user's caloric needs and food
preferences. It utilizes natural language processing to generate creative meal ideas using ingredients selected by the
algorithm.

## Features

- Calculation of daily calorie needs based on user inputs like age, height, weight, and gender
- Selection of user food preferences and allergies/restrictions
- Generation of meal plans for breakfast, lunch, and dinner within the target calorie ranges
- Creative naming and description of meals using natural language generation
- Meal Generation using Anthropic's Claude AI assistant

## Technology

- Python
- Streamlit for app UI
- Pandas for data manipulation
- Anthropic Claude API for NLP completions

The app calculates the user's basal metabolic rate to determine their daily calorie needs. It then randomly selects
ingredients from categorized food items to meet the calorie targets for each meal. The selected ingredients are passed
to the Claude AI to generate creative names and descriptions for the meals.

The project demonstrates an application of AI for personalized meal planning and natural language generation. It could
be extended by adding user accounts, more food options, recipe instructions etc.