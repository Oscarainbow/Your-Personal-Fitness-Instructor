import pandas as pd
import os

# Function to load food data from CSV
def load_food_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "data", "foodData", "food.csv")
    
    df = pd.read_csv(csv_file)
    
    required_columns = ['Description', 'Data.Carbohydrate', 'Data.Protein', 'Data.Fat.Total Lipid']
    df = df[required_columns].fillna(0)
    
    # Compute calories per 100g
    df['Calories_per_100g'] = (df['Data.Carbohydrate'] * 4) + (df['Data.Protein'] * 4) + (df['Data.Fat.Total Lipid'] * 9)
    # Create a dictionary {food_name (lowercase): calories per 100g}
    return dict(zip(df['Description'].str.lower(), df['Calories_per_100g']))

# Function to load exercise data from CSV
def load_exercise_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "data", "exerciseData", "exercise_dataset.csv")

    df = pd.read_csv(csv_file)

    # Clean column names
    df.columns = ['Activity', '130_lb', '155_lb', '180_lb', '205_lb', 'Calories_per_kg']

    # Convert activity names to lowercase for better matching
    df['Activity'] = df['Activity'].str.lower().str.strip()

    return df

# Function to calculate calories based on food name and weight in grams
def get_calories(food_name, weight_in_grams, food_dict):
    food_name = food_name.lower().strip()

    if food_name in food_dict:
        calories_per_100g = food_dict[food_name]
        total_calories = (calories_per_100g / 100) * weight_in_grams
        return round(total_calories, 2)
    
    return None

#Function to calculate calorie intake on average someone should take
def calculate_bmr(gender, weight, height, age):
    if gender.lower() == 'female':
        bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
    elif gender.lower() == 'male':
        bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    return bmr
#Function to calculate if you are gaining or losing weight
def assess_weight_change(gender, weight, height, age, daily_food_intake):
    food_dict = load_food_data()
    
    total_calories_consumed = 0
    for food, weight in daily_food_intake.items():
        calories = get_calories(food, weight, food_dict)
        if calories is not None:
            print(f"{food}: {calories} kcal")  # Debugging statement
            total_calories_consumed += calories
        else:
            print(f"Warning: {food} not found in food data. Try a more specific name.")  # Debugging statement
    
    print(f"Total calories consumed: {total_calories_consumed}")  # Debugging statement
    
    bmr = calculate_bmr(gender, weight, height, age)
    print(f"Calculated BMR: {bmr:.2f}")  # Debugging statement
    
    if total_calories_consumed > bmr:
        return f"You are consuming {total_calories_consumed} calories, which is more than your BMR of {bmr:.2f}. You are likely gaining weight."
    elif total_calories_consumed < bmr:
        return f"You are consuming {total_calories_consumed} calories, which is less than your BMR of {bmr:.2f}. You are likely losing weight."
    else:
        return f"Your calorie intake matches your BMR of {bmr:.2f}, so your weight is likely stable."
# Main function for testing
def main():
    food_data = load_food_data()
    
    food_name = input("Enter food name: ")
    try:
        weight = float(input("Enter weight in grams: "))
        calories = get_calories(food_name, weight, food_data)
        
        if calories is not None:
            print(f"Calories for {weight}g of {food_name}: {calories} kcal")
        else:
            print("Food not found. Check spelling and try again.")
    
    except ValueError:
        print("Invalid input! Please enter a number for weight.")

    gender = "female"
    weight = 70  # kg
    height = 170  # cm
    age = 30  # years

    bmr_value = calculate_bmr(gender, weight, height, age)
    print(f"Basal Metabolic Rate (BMR): {bmr_value:.2f} kcal")
    gender = "male"
    weight = 70  # kg
    height = 175  # cm
    age = 25
    daily_food_intake = {
        "Apple, raw": 200,  # grams
        "Chicken breast, grilled without sauce, skin eaten": 150,
        "Rice, white, with lentils, fat added": 250
    }
    
    result = assess_weight_change(gender, weight, height, age, daily_food_intake)
    print(result)
    

    sport = input("Enter sport/activity: ")
    try:
        duration = float(input("Enter duration in minutes: "))
        weight_kg = float(input("Enter your weight in kg: "))
        
        calories_burned = calculate_calories_burned(sport, duration, weight_kg, exercise_data)
        
        if calories_burned is not None:
            print(f"Calories burned for {duration} minutes of {sport}: {calories_burned} kcal")
        else:
            print("Activity not found. Check spelling and try again.")
    
    except ValueError:
        print("Invalid input! Please enter valid numbers.")
    gender = "male"
    weight = 70  # kg
    height = 175  # cm
    age = 25
    daily_food_intake = {
        "raw apple": 200,  # grams
        "grilled chicken breast": 150,
        "white rice": 250
    }
    
    result = assess_weight_change(gender, weight, height, age, daily_food_intake)
    print(result)
# Run the main function if script is executed directly
if __name__ == "__main__":
    main()
