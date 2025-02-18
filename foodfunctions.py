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

# Function to calculate calorie intake on average someone should take
def calculate_bmr(gender, weight, height, age):
    if gender.lower() == 'female':
        bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
    elif gender.lower() == 'male':
        bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    return bmr

# Function to calculate calories burned based on sport, time, and weight
def calculate_calories_burned(sport, duration_in_minutes, weight_in_kg, exercise_df):
    sport = sport.lower().strip()
    
    # Find the sport in the dataset
    match = exercise_df[exercise_df['Activity'].str.contains(sport, na=False)]
    
    if match.empty:
        return None  # Sport not found
    
    # Use the 'Calories_per_kg' column to compute burned calories
    calories_per_kg_per_hour = match.iloc[0]['Calories_per_kg']
    calories_burned = calories_per_kg_per_hour * weight_in_kg * (duration_in_minutes / 60)
    
    return round(calories_burned, 2)

# Main function for testing
def main():
    food_data = load_food_data()
    exercise_data = load_exercise_data()

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

# Run the main function if script is executed directly
if __name__ == "__main__":
    main()
