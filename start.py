import requests
import random

def get_50_random():
    API_KEY = "58dd44bca546441e951e61b251f0a8bb"

    URL = f"https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&number=10&includeNutrition=true"

    response = requests.get(URL)

    if response.status_code == 200:
        #Parse json and get list of recipes
        data = response.json()
        recipes = data.get("recipes", [])

        #print each recipe title along with macronutrients(calories,protein,fat,carb)
        if recipes:
            for idx, recipe in enumerate(recipes, 1):
                title = recipe.get('title', 'Unknown Title')
                nutrients = recipe.get('nutrition', {}).get('nutrients', [])

                def find_nutrient(nutrient_name):
                    nutrient = next((item for item in nutrients if item.get('name') == nutrient_name), None)
                    return nutrient.get('amount', 'Unknown') if nutrient else 'Unknown'
                
                calories = find_nutrient('Calories')
                protein = find_nutrient('Protein')
                fat = find_nutrient('Fat')
                carbs = find_nutrient('Carbohydrates')

                print(f"Recipe {idx}: {title}")
                print(f"    Calories: {calories} kcal")
                print(f"    Protein: {protein} g")
                print(f"    Fat: {fat} g")
                print(f"    Carbohydrates: {carbs} g\n")
        else:
            print("No food items found grrr")
    else:
        print(f"Error: UInable to retreieve food data (status code: {response.status_code})")


def get_user_info():
    print("Welcome to my nutrition planner!")
    print("To get started please enter some information.")

    #get gender to use in equation, only 2 options as it is based
    #on basal metabolic rate and is determined by male or female
    user_gender = input("Please enter your gender (m/f) : ")
    while user_gender.lower() not in ['m','f']:
        user_gender = input("Please enter m or f : ")

    #get user weight until a valid weight is entered
    user_weight = input("Please enter your weight in pounds : ")
    while user_weight.isdigit() == False or int(user_weight) < 0 or int(user_weight) > 600:
        user_weight = input("Please enter a valid weight: ")
    user_weight = int(user_weight) / 2.20462
    print(user_weight)

    #get user height until a valid height is entered
    print("Please enter your height: ")
    user_height_feet = input("Feet: ")
    user_height_inches = input("Inches: ")
    while user_height_feet.isdigit() == False or user_height_inches.isdigit() == False or (int(user_height_feet) * 12 + int(user_height_inches)) < 0 or (int(user_height_feet) * 12 + int(user_height_inches)) > 150:
        print("Please enter a valid height: ")
        user_height_feet = input("Feet: ")
        user_height_inches = input("Inches: ")
    user_height = int(user_height_feet) * 12 + int(user_height_inches)
    user_height *= 2.54
    print(user_height)

    #get user weight until a valid weight is entered
    user_age = input("Please enter your age : ")
    while user_age.isdigit() == False or int(user_age) < 0 or int(user_age) > 100:
        user_age = input("Please enter a valid age: ")
    user_age = int(user_age)

    #Calculate basasl metabolic rate using Mifflin-St Jeor Equation
    basal_metabolic_rate = 0
    if user_gender == 'm':
        basal_metabolic_rate = (10 * user_weight) + (6.25 * user_height) - (5 * user_age) + 5
    else:
        basal_metabolic_rate = (10 * user_weight) + (6.25 * user_height) - (5 * user_age) - 161

    print(f"Your basal metabolic rate is: {basal_metabolic_rate}\n")

    print("1: Little to no exercise")
    print("2: Exercise 1-3 times/week")
    print("3: Exercise 4-5 times/week")
    print("4: Daily exercise or intense exercise 3-4 times/week	")
    print("5: Intense exercise 6-7 times/week")
    print("6: Very intense exercise daily, or physical job")
    exercise_level = input("Please choose a number that represents your level of activity: ")
    while exercise_level.isdigit() == False or int(exercise_level) > 6 or int(exercise_level) < 1:
        exercise_level = input("Please choose a number 1-6: ")
    exercise_level = int(exercise_level)

    total_BMR = basal_metabolic_rate * (((1.9-1.2)/5) * (exercise_level-1) + 1.2)

    print(f"Your total basal metabolic rate is: {total_BMR}\n")

    get_50_random()



get_user_info()