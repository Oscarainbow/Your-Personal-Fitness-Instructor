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

**test_calculate_bmr_X**
Tests: Various valid and invalid inputs to calculate_bmr
Code Covered: BMR calculation for male and female, input validation, error handling for None values
Validation: Valid inputs return expected results; invalid/missing values raise appropriate exceptions (TypeError, AttributeError)

**test_assess_weight_change_X**
Tests: Valid inputs for males and females, and invalid scenarios with missing required fields
Code Covered: Full calorie intake evaluation, BMR computation, dictionary parsing, input validation
Validation: Ensures all expected keys (status, message, bmr, food_summary) are in the response; exception raised when required fields are missing

**test_record_daily_X**
Tests: Logging daily activity and nutrition with complete and incomplete inputs
Code Covered: Request handling for /record-daily, validation of required fields, default handling for empty lists
Validation: Valid input returns 200 and a success message; missing required fields trigger 400 with error; empty food/exercise still allows submission

**test_monthly_summary_X**
Tests: Summary retrieval with valid user data, missing params, and nonexistent users
Code Covered: Monthly aggregation logic, input validation, error responses for missing or unregistered users
Validation: Valid inputs yield full summary; missing fields result in 400; no data returns 404 with clear error
