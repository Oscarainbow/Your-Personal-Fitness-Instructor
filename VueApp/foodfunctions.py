from flask import Flask, request, jsonify
import pandas as pd
import os
import json
from flask_cors import CORS  # Import CORS
from collections import defaultdict
from datetime import datetime

# This stores daily records: {user_id: [{date, food, exercise, total_calories_in, total_calories_out}]}
user_calorie_log = defaultdict(list)


app = Flask(__name__)
CORS(app)

# Function to load food data from CSV
def load_food_data():

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Get parent directory
    csv_file = os.path.join(BASE_DIR, "data", "foodData", "food.csv")



    
    df = pd.read_csv(csv_file)
    
    required_columns = ['Description', 'Data.Carbohydrate', 'Data.Protein', 'Data.Fat.Total Lipid']
    df = df[required_columns].fillna(0)
    
    # Compute calories per 100g
    df['Calories_per_100g'] = (df['Data.Carbohydrate'] * 4) + (df['Data.Protein'] * 4) + (df['Data.Fat.Total Lipid'] * 9)
    # Create a dictionary {food_name (lowercase): calories per 100g}
    return dict(zip(df['Description'].str.lower(), df['Calories_per_100g']))

# Function to get food names
@app.route('/food-names', methods=['GET'])
def get_food_names():
    food_dict = load_food_data()
    return jsonify(sorted(food_dict.keys()))

# Function to load exercise data from CSV
def load_exercise_data():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Get parent directory
    csv_file = os.path.join(BASE_DIR, "data", "exerciseData", "exercise_dataset.csv")

    df = pd.read_csv(csv_file)

    # Clean column names
    df.columns = ['Activity', '130_lb', '155_lb', '180_lb', '205_lb', 'Calories_per_kg']

    # Convert activity names to lowercase for better matching
    df['Activity'] = df['Activity'].str.lower().str.strip()

    return df

# Function to get exercise names
@app.route('/exercise-names', methods=['GET'])
def get_exercise_names():
    df = load_exercise_data()
    activities = df['Activity'].dropna().unique()
    return jsonify(sorted(activities.tolist()))

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

@app.route('/record-daily', methods=['POST'])
def record_daily():
    data = request.json
    user_id = data.get("user_id")
    gender = data.get("gender")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    food_entries = data.get("daily_food_intake", [])
    exercise_entries = data.get("daily_exercise", [])  # list of {"activity": ..., "duration_mins": ...}
    
    if not all([user_id, gender, weight, height, age]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Load food and exercise data
    food_dict = load_food_data()
    exercise_df = load_exercise_data()
    
    # Calculate intake
    total_calories_in = 0
    for item in food_entries:
        cal = get_calories(item.get("food"), item.get("weight"), food_dict)
        if cal:
            total_calories_in += cal
    
    # Calculate burned calories (out)
    total_calories_out = 0
    for entry in exercise_entries:
        activity = entry.get("activity", "").lower()
        duration = entry.get("duration_mins", 0)
        match = exercise_df[exercise_df["Activity"] == activity]
        if not match.empty:
            cal_per_kg_per_min = match.iloc[0]["Calories_per_kg"] / 60
            total_calories_out += cal_per_kg_per_min * weight * duration

    # Store the data
    today = datetime.now().strftime("%Y-%m-%d")
    user_calorie_log[user_id].append({
        "date": today,
        "food": food_entries,
        "exercise": exercise_entries,
        "total_calories_in": round(total_calories_in, 2),
        "total_calories_out": round(total_calories_out, 2)
    })

    return jsonify({"message": "Daily record saved successfully."})

@app.route('/monthly-summary', methods=['GET'])
def monthly_summary():
    user_id = request.args.get("user_id")
    weight = float(request.args.get("weight", 0))

    if not user_id or not weight:
        return jsonify({"error": "Missing user ID or weight"}), 400

    records = user_calorie_log.get(user_id, [])
    if not records:
        return jsonify({"error": "No data found for user."}), 404

    total_in = sum(r["total_calories_in"] for r in records)
    total_out = sum(r["total_calories_out"] for r in records)

    # Net calorie difference
    net_deficit = total_out - total_in

    # 7700 kcal ≈ 1 kg fat loss
    weight_change_kg = net_deficit / 7700

    return jsonify({
        "total_days": len(records),
        "total_calories_in": round(total_in, 2),
        "total_calories_out": round(total_out, 2),
        "net_deficit": round(net_deficit, 2),
        "estimated_weight_change_kg": round(weight_change_kg, 2)
    })




# Main function to start the Flask app
def main():
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
    

