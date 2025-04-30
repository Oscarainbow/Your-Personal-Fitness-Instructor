## Testing Code Coverage

**test_bmr_endpoint**
Tests: valid POST to /bmr with parameters
Code Covered: Endpoints, BMR calculation functionlity for Male
Validation: Ensures a 200 response, asserts bmr is in the response


**test_bmr_missing_params**
Tests: POST to /bmr with *missing* parameters
Code Covvered: Error handeling for missing JSON keys
Validation: Results in a Bad Request (400)


**test_weight_change_endpoint**
Tests: Valid Weight Change response with parameters
Code Covered: Input parsing, Weight Change functionality, BMR and Calorie calculation
Validation: Asserts status, total_calories in response.


**test_weight_change_missing_fields**
Tests: Weight Change with missing 'daily_food_intake' parameter
Code Covered: Fallback or Default Value handling
Validation: Ensures a 200 response, functions despite missing input


**test_get_calories_X**
Tests: Two examples of food items, apples and bananas, and possibility of missing parameter
Code Covered: Guaranteed functionality of the items 'apple' and 'banana', assumed functionality of other food items in the database, Error Handling


