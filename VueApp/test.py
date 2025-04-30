import unittest
import json
from foodfunctions import app, get_calories  
from foodfunctions import calculate_bmr
from foodfunctions import assess_weight_change

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
    
    def test_bmr_endpoint(self):
        response = self.client.post('/bmr', json={
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("bmr", data)

    def test_bmr_missing_params(self):
        response = self.client.post('/bmr', json={
            "gender": "male",
            "weight": 70
        })
        self.assertEqual(response.status_code, 400)

    def test_weight_change_endpoint(self):
        response = self.client.post('/weight-change', json={
            "gender": "female",
            "weight": 60,
            "height": 160,
            "age": 30,
            "daily_food_intake": [
                {"food": "apple", "weight": 200}
            ]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("status", data)
        self.assertIn("total_calories", data)

    # Missing daily food intake
    def test_weight_change_missing_fields(self):
        response = self.client.post('/weight-change', json={
            "gender": "female",
            "weight": 60,
            "height": 160,
            "age": 30
        })
        self.assertEqual(response.status_code, 200)
    
    # Test get_calories
    def test_get_calories_apple_valid(self):
        food_dict = {"apple": 52.0}
        result = get_calories("apple", 150, food_dict)
        expected = round((52.0 / 100) * 150, 2)
        self.assertEqual(result, expected)

    def test_get_calories_banana_valid(self):
        food_dict = {"banana": 89.0}
        result = get_calories("banana", 120, food_dict)
        expected = round((89.0 / 100) * 120, 2)
        self.assertEqual(result, expected)

    def test_get_calories_missing_food_name(self):
        food_dict = {"apple": 52.0}
        result = get_calories("", 100, food_dict)  
        self.assertIsNone(result)

    def test_get_calories_missing_weight(self):
        food_dict = {"banana": 89.0}
        result = get_calories("banana", 0, food_dict)  
        expected = 0.0
        self.assertEqual(result, expected)

    def test_get_calories_both_values_empty_or_zero(self):
        food_dict = {"apple": 52.0, "banana": 89.0}
        result = get_calories("", 0, food_dict)  
        self.assertIsNone(result)

    # Test calc bmr
    def test_calculate_bmr_male(self):
        result = calculate_bmr("male", 70, 175, 25)
        expected = 66 + (13.7 * 70) + (5 * 175) - (6.8 * 25)
        self.assertEqual(result, expected)

    def test_calculate_bmr_female(self):
        result = calculate_bmr("female", 60, 165, 30)
        expected = 655 + (9.6 * 60) + (1.8 * 165) - (4.7 * 30)
        self.assertEqual(result, expected)

    def test_calculate_bmr_none_gender(self):
        with self.assertRaises(AttributeError):  
            calculate_bmr(None, 70, 175, 25)

    def test_calculate_bmr_none_weight(self):
        with self.assertRaises(TypeError):
            calculate_bmr("male", None, 175, 25)

    def test_calculate_bmr_none_height(self):
        with self.assertRaises(TypeError):
            calculate_bmr("male", 70, None, 25)

    def test_calculate_bmr_none_age(self):
        with self.assertRaises(TypeError):
            calculate_bmr("male", 70, 175, None)

# Test assess_weight_change
    def test_assess_weight_change_male(self):
        result = assess_weight_change(
            gender="male",
            weight=75,
            height=180,
            age=28,
            daily_food_intake=[
                {"food": "apple", "weight": 200},  
                {"food": "banana", "weight": 150}
            ]
        )
        self.assertIn("status", result)
        self.assertIn("total_calories", result)
        self.assertIn("message", result)
        self.assertIn("food_summary", result)

    def test_assess_weight_change_female(self):
        result = assess_weight_change(
            gender="female",
            weight=60,
            height=165,
            age=32,
            daily_food_intake=[
                {"food": "apple", "weight": 100}
            ]
        )
        self.assertIn("status", result)
        self.assertIn("bmr", result)
        self.assertIn("total_calories", result)

    def test_assess_weight_change_none_gender(self):
        with self.assertRaises(AttributeError):  
            assess_weight_change(
                gender=None,
                weight=60,
                height=165,
                age=32,
                daily_food_intake=[{"food": "apple", "weight": 100}]
            )

    def test_assess_weight_change_none_weight(self):
        with self.assertRaises(TypeError):  
            assess_weight_change(
                gender="female",
                weight=None,
                height=165,
                age=32,
                daily_food_intake=[{"food": "apple", "weight": 100}]
            )

    def test_assess_weight_change_none_height(self):
        with self.assertRaises(TypeError):  
            assess_weight_change(
                gender="female",
                weight=60,
                height=None,
                age=32,
                daily_food_intake=[{"food": "apple", "weight": 100}]
            )

    def test_assess_weight_change_none_age(self):
        with self.assertRaises(TypeError):  
            assess_weight_change(
                gender="female",
                weight=60,
                height=165,
                age=None,
                daily_food_intake=[{"food": "apple", "weight": 100}]
            )
# Test record_daily
    def test_record_daily_valid(self):
        response = self.client.post('/record-daily', json={
            "user_id": "testuser1",
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25,
            "daily_food_intake": [{"food": "apple", "weight": 200}],
            "daily_exercise": [{"activity": "running", "duration_mins": 30}]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)

    def test_record_daily_missing_user_id(self):
        response = self.client.post('/record-daily', json={
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25,
            "daily_food_intake": [{"food": "apple", "weight": 200}],
            "daily_exercise": [{"activity": "running", "duration_mins": 30}]
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_record_daily_missing_gender(self):
        response = self.client.post('/record-daily', json={
            "user_id": "testuser2",
            "weight": 70,
            "height": 175,
            "age": 25,
            "daily_food_intake": [{"food": "apple", "weight": 200}],
            "daily_exercise": [{"activity": "running", "duration_mins": 30}]
        })
        self.assertEqual(response.status_code, 400)

    def test_record_daily_missing_weight(self):
        response = self.client.post('/record-daily', json={
            "user_id": "testuser3",
            "gender": "female",
            "height": 160,
            "age": 30,
            "daily_food_intake": [{"food": "banana", "weight": 150}],
            "daily_exercise": []
        })
        self.assertEqual(response.status_code, 400)

    def test_record_daily_missing_height(self):
        response = self.client.post('/record-daily', json={
            "user_id": "testuser4",
            "gender": "male",
            "weight": 80,
            "age": 35,
            "daily_food_intake": [],
            "daily_exercise": []
        })
        self.assertEqual(response.status_code, 400)

    def test_record_daily_missing_age(self):
        response = self.client.post('/record-daily', json={
            "user_id": "testuser5",
            "gender": "male",
            "weight": 80,
            "height": 180,
            "daily_food_intake": [],
            "daily_exercise": []
        })
        self.assertEqual(response.status_code, 400)

    def test_record_daily_empty_food_and_exercise(self):
        response = self.client.post('/record-daily', json={
            "user_id": "testuser6",
            "gender": "female",
            "weight": 65,
            "height": 160,
            "age": 27,
            "daily_food_intake": [],
            "daily_exercise": []
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)

# Test monthly_summary
    def test_monthly_summary_valid(self):
        self.client.post('/record-daily', json={
            "user_id": "summary_user",
            "gender": "male",
            "weight": 75,
            "height": 180,
            "age": 30,
            "daily_food_intake": [{"food": "apple", "weight": 100}],
            "daily_exercise": [{"activity": "running", "duration_mins": 20}]
        })

        response = self.client.get('/monthly-summary?user_id=summary_user&weight=75')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("total_days", data)
        self.assertIn("total_calories_in", data)
        self.assertIn("total_calories_out", data)
        self.assertIn("net_deficit", data)
        self.assertIn("estimated_weight_change_kg", data)

    def test_monthly_summary_missing_user_id(self):
        response = self.client.get('/monthly-summary?user_id=&weight=70')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_monthly_summary_missing_weight(self):
        response = self.client.get('/monthly-summary?user_id=testuser')  
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_monthly_summary_user_with_no_data(self):
        response = self.client.get('/monthly-summary?user_id=nonexistent_user&weight=70')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main()
