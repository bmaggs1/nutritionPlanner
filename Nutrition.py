import requests
from dotenv import load_dotenv
import os

load_dotenv()
#Environment Variables
API_KEY = os.getenv("API_KEY")


def get_50_random(user):
    daily_cals = user.daily_calories
    if daily_cals > 2800:
        d_meals = 4
    else: 
        d_meals = 3

    d_protein = (daily_cals * 0.30) / 4
    d_carbs = (daily_cals * 0.50) / 4
    d_fat = (daily_cals * 0.20) / 9
    
    print(f"Cals = {daily_cals}, p: {d_protein}, c: {d_carbs}, f:{d_fat}, {d_meals} meals a day")
    print(f"{d_carbs/d_meals} carbs a meal, {d_protein/d_meals} protein a meal, {d_fat/d_meals} fat a meal")
    base_url = "https://api.spoonacular.com/recipes/findByNutrients?"
    params = (
        f"minCarbs={d_carbs/d_meals - 30}&"
        f"maxCarbs={d_carbs/d_meals + 30}&"
        f"minProtein={d_protein/d_meals - 30}&"
        f"maxProtein={d_protein/d_meals + 30}&"
        f"minFat={d_fat/d_meals - 15}&"
        f"maxFat={d_fat/d_meals + 15}&"
        f"number={10}&"
        f"apiKey={API_KEY}"
    )

    URL = base_url + params

    response = requests.get(URL)

    if response.status_code == 200:
        #Parse json and get list of recipes
        data = response.json()
        recipes = []
        for item in data:
            recipes.append(item)
            #print(item)
        

        #print each recipe title along with macronutrients(calories,protein,fat,carb)
        if recipes:
            for idx, recipe in enumerate(recipes, 1):
                title = recipe.get('title', 'Unknown Title')
                nutrients = recipe.get('nutrition', {}).get('nutrients', [])

                def find_nutrient(nutrient_name):
                    nutrient = next((item for item in nutrients if item.get('name') == nutrient_name), None)
                    return nutrient.get('amount', 'Unknown') if nutrient else 'Unknown'
                
                calories = recipe.get('calories')
                protein = recipe.get('protein')
                fat = recipe.get('fat')
                carbs = recipe.get('carbs')

                print(f"Recipe {idx}: {title}")
                print(f"    Calories: {calories} kcal")
                print(f"    Protein: {protein} g")
                print(f"    Fat: {fat} g")
                print(f"    Carbohydrates: {carbs} g\n")
        else:
            print("No food items found grrr")
    else:
        print(f"Error: UInable to retreieve food data (status code: {response.status_code})")
