import requests
import random

class User:
    def __init__(self, gender, weight, height, age, activity_level, nutritition_goal):
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.activity_level = activity_level
        self.nutrition_goal = nutritition_goal
        self.daily_calories = self.calculate_daily_calories()

        def calculate_daily_calories(self):
            if self.gender == 'm':
                base_bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
            else:
                base_bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
            tot_bmr = base_bmr * (((1.9 - 1.2) / 5) * (self.activity_level - 1) + 1.2)
            dailyCals = tot_bmr + (200 * (self.nutrition_goal - 3))
            return dailyCals    
        
        @staticmethod
        def from_dict(data):
            return User(
                gender = data['gender'],
                weight = data['weight'],
                height = data['height'],
                age = data['age'],
                activity_level = data['activity_level'],
                nutritition_goal = data['nutrition_goal']
            )

def save_user_data(user):
    with open('user_data.json', 'w') as file:
        json.dump(user.to_dict(), file)
    print("User data saved successfully.")

def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            data = json.load(file)
            return User.from_dict(data)
    return None

def get_50_random():
    API_KEY = "u thought! ( dont check previous commits )"

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


    #calculate total metabolic rate after exercise
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

    #Prompt the user for their plan of action moving forward.
    print("Please select your nutrition goal:")
    print("1: Lose 1 pound a week")
    print("2: Lose half a pound a week")
    print("3: Maintain weight")
    print("4: Gain half a pound a week")
    print("5: Gain 1 pound a week")
    nutrition_goal = input("Please enter your age : ")
    while nutrition_goal.isdigit() == False or int(nutrition_goal) < 1 or int(nutrition_goal) > 5:
        nutrition_goal = input("Please enter a valid choice: ")
    nutrition_goal = int(user_age)

    goal_cals = total_BMR + (200 * (nutrition_goal - 3))

    print(f"Your daily calorie intake should be {goal_cals} calories.")

    user = User(user_gender, user_weight, user_height, user_age, exercise_level, nutrition_goal)

    return user

def main():
    user = load_user_data()

    if not user:
        user = get_user_info()
        save_user_data(user)
    else:
        print(f"Welcome back! Here are your stored details:")
        print(f"Gender: {user.gender}")
        print(f"Weight: {user.weight} kg")
        print(f"Height: {user.height} cm")
        print(f"Age: {user.age}")
        print(f"Activity Level: {user.activity_level}")
        print(f"Nutrition Goal: {user.nutrition_goal}")
        print(f"Your daily calorie intake should be: {user.daily_calories} kcal/day\n")

    get_50_random()



get_user_info()
if __name__ == "__main__":
    main()
