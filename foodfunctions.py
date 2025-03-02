from flask import Flask, request, jsonify
import pandas as pd
import os
import json

app = Flask(__name__)

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

#Function to run calculate_bmr in Vue
@app.route('/bmr', methods=['POST'])
def get_bmr():
    data = request.json
    gender = data.get("gender")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")

    if not all([gender, weight, height, age]):
        return jsonify({"error": "Missing parameters"}), 400

    bmr = calculate_bmr(gender, weight, height, age)
    return jsonify({"bmr": round(bmr, 2)})

#Function to calculate if you are gaining or losing weight
def assess_weight_change(gender, weight, height, age, daily_food_intake):
    food_dict = load_food_data()
    
    total_calories_consumed = 0
    food_summary = []  # Store details of each food item

    for food_entry in daily_food_intake:
        food_name = food_entry.get("food")
        food_weight = food_entry.get("weight")

        if not food_name or not food_weight:
            continue  # Skip if missing food name or weight

        calories = get_calories(food_name, food_weight, food_dict)
        if calories is not None:
            food_summary.append({"food": food_name, "weight": food_weight, "calories": calories})
            total_calories_consumed += calories
        else:
            print(f"Warning: {food_name} not found in food data. Try a more specific name.")  # Debugging statement
    
    print(f"Total calories consumed: {total_calories_consumed}")  # Debugging statement
    
    bmr = calculate_bmr(gender, weight, height, age)
    print(f"Calculated BMR: {bmr:.2f}")  # Debugging statement
    
    if total_calories_consumed > bmr:
        status = "gaining weight"
        message = f"You are consuming {total_calories_consumed} calories, which is more than your BMR of {bmr:.2f}. You are likely gaining weight."
    elif total_calories_consumed < bmr:
        status = "losing weight"
        message = f"You are consuming {total_calories_consumed} calories, which is less than your BMR of {bmr:.2f}. You are likely losing weight."
    else:
        status = "maintaining weight"
        message = f"Your calorie intake matches your BMR of {bmr:.2f}, so your weight is likely stable."

    return {
        "status": status,
        "bmr": round(bmr, 2),
        "total_calories": round(total_calories_consumed, 2),
        "food_summary": food_summary,
        "message": message
    }

@app.route('/weight-change', methods=['POST'])
def weight_change():
    data = request.json
    gender = data.get("gender")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    daily_food_intake = data.get("daily_food_intake", [])  # Expecting a list of food items

    # Ensure all required fields are present and valid
    if not all([gender, weight, height, age]) or not isinstance(daily_food_intake, list):
        return jsonify({"error": "Missing parameters or incorrect format"}), 400

    # Call the function with the provided data
    result = assess_weight_change(gender, weight, height, age, daily_food_intake)

    return jsonify(result)  # Directly return the structured JSON response



# Main function to start the Flask app
def main():
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()

