import requests
from dotenv import load_dotenv
import os

load_dotenv()
#Environment Variables
API_KEY = os.getenv("API_KEY")


def get_50_random():
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

get_50_random()