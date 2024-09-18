import os, json, hashlib
import Nutrition

nutrition_goals = {
    '1': 'Lose 1 pound a week',
    '2': 'Lose 0.5 pound a week',
    '3': 'Maintain weight',
    '4': 'Gain 0.5 pound a week',
    '5': 'Gain 1 pound a week'
}
activity_levels = {
    '1': 'Little to no exercise',
    '2': 'Exercise 1-3 times/week',
    '3': 'Exercise 4-5 times/week',
    '4': 'Daily exercise or intense exercise 3-4 times/week',
    '5': 'Intense exercise 6-7 times/week',
    '6': 'Very intense exercise daily, or physical job'
}

class User:
    def calculate_daily_calories(self):
        if self.gender == 'm':
            base_bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            base_bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        tot_bmr = base_bmr * (((1.9 - 1.2) / 5) * (self.activity_level - 1) + 1.2)
        dailyCals = tot_bmr + (200 * (self.nutrition_goal - 3))
        return dailyCals

    def __init__(self, name, gender, weight, height, age, activity_level, nutritition_goal):
        self.name = name
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.activity_level = activity_level
        self.nutrition_goal = nutritition_goal
        self.daily_calories = self.calculate_daily_calories()
    
    def to_dict(self):
        """Convert user data to a dictionary for saving to JSON"""
        return {
            'name': self.name,
            'gender': self.gender,
            'weight': self.weight,
            'height': self.height,
            'age': self.age,
            'activity_level': self.activity_level,
            'nutrition_goal': self.nutrition_goal
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            name = data['name'],
            gender = data['gender'],
            weight = data['weight'],
            height = data['height'],
            age = data['age'],
            activity_level = data['activity_level'],
            nutritition_goal = data['nutrition_goal']
        )

def hash_name(name):
    # Hash the name using SHA-1
    sha1_hash = hashlib.sha1(name.encode()).hexdigest()
    # Truncate the hash to 20 characters
    return sha1_hash[:20]

def save_user_data(user):
    hashed_name = hash_name(user.name)
    with open(f'{hashed_name}_data.json', 'w') as file:
        json.dump(user.to_dict(), file)
    print("User data saved successfully.")

def load_user_data(name):
    hashed_name = hash_name(name)
    if os.path.exists(f'{hashed_name}_data.json'):
        with open(f'{hashed_name}_data.json', 'r') as file:
            data = json.load(file)
            return User.from_dict(data)
    return None

def get_user_info(name):
    print("Welcome to my nutrition planner!")
    print("To get started please enter some information.")

    #get gender to use in equation, only 2 options as it is based
    #on basal metabolic rate and is determined by male or female
    user_gender = input("Please enter your gender (m/f):  ")
    while user_gender.lower() not in ['m','f']:
        user_gender = input("Please enter m or f:  ")
    print()

    #get user weight until a valid weight is entered
    user_weight = input("Please enter your weight in pounds:  ")
    while user_weight.isdigit() == False or int(user_weight) < 0 or int(user_weight) > 600:
        user_weight = input("Please enter a valid weight:  ")
    user_weight = int(user_weight) / 2.20462
    print()

    #get user height until a valid height is entered
    print("Please enter your height:  ")
    user_height_feet = input("Feet:  ")
    user_height_inches = input("Inches:  ")
    while user_height_feet.isdigit() == False or user_height_inches.isdigit() == False or (int(user_height_feet) * 12 + int(user_height_inches)) < 0 or (int(user_height_feet) * 12 + int(user_height_inches)) > 150:
        print("Please enter a valid height:  ")
        user_height_feet = input("Feet:  ")
        user_height_inches = input("Inches:  ")
    user_height = int(user_height_feet) * 12 + int(user_height_inches)
    user_height *= 2.54
    print()

    #get user weight until a valid weight is entered
    user_age = input("Please enter your age:  ")
    while user_age.isdigit() == False or int(user_age) < 0 or int(user_age) > 100:
        user_age = input("Please enter a valid age:  ")
    user_age = int(user_age)
    print()

    #Calculate basasl metabolic rate using Mifflin-St Jeor Equation
    basal_metabolic_rate = 0
    if user_gender == 'm':
        basal_metabolic_rate = (10 * user_weight) + (6.25 * user_height) - (5 * user_age) + 5
    else:
        basal_metabolic_rate = (10 * user_weight) + (6.25 * user_height) - (5 * user_age) - 161


    #calculate total metabolic rate after exercise
    for num in activity_levels:
        print(num, activity_levels.get(num))
    exercise_level = input("Please choose a number that represents your level of activity:  ")
    while exercise_level.isdigit() == False or int(exercise_level) > 6 or int(exercise_level) < 1:
        exercise_level = input("Please choose a number 1-6:  ")
    exercise_level = int(exercise_level)
    total_BMR = basal_metabolic_rate * (((1.9-1.2)/5) * (exercise_level-1) + 1.2)
    print()

    #Prompt the user for their plan of action moving forward.
    for num in nutrition_goals:
        print(num, nutrition_goals.get(num))
    nutrition_goal = input("Please enter your preferred nutrition goal:  ")
    while nutrition_goal.isdigit() == False or int(nutrition_goal) < 1 or int(nutrition_goal) > 5:
        nutrition_goal = input("Please enter a valid choice:  ")
    nutrition_goal = int(nutrition_goal)
    goal_cals = total_BMR + (200 * (nutrition_goal - 3))
    user = User(name, user_gender, user_weight, user_height, user_age, exercise_level, nutrition_goal)
    print()


    print(f"Your basal metabolic rate is: {basal_metabolic_rate}")
    print(f"Your total basal metabolic rate is: {total_BMR}")
    print(f"Your daily calorie intake should be {goal_cals} calories.\n")


    return user

def main():
    name = input('Welcome!\nPlease enter your name to get started:  ')
    name = name.lower()
    user = load_user_data(name)

    if not user:
        user = get_user_info(name)
        save_user_data(user)
    else:
        print(f"Welcome back! Here are your stored details:")
        print(f"Weight: {user.weight} kg")
        print(f"Height: {user.height} cm")
        print(f"Age: {user.age}")
        print(f"Activity Level: {activity_levels.get(user.activity_level)}")
        print(f"Nutrition Goal: {nutrition_goals.get(user.nutrition_goal)}")
        print(f"Your current daily calorie intake should be: {user.daily_calories} kcal/day")

    Nutrition.get_50_random(user)



if __name__ == "__main__":
    main()
