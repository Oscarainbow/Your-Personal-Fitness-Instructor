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

# Run the main function if script is executed directly
if __name__ == "__main__":
    main()