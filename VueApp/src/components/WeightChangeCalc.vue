<template>
  <div class="container">
    <h2>Weight Change Calculator</h2>
    
    <label>Gender:</label>
    <select v-model="gender">
      <option value="male">Male</option>
      <option value="female">Female</option>
    </select>

    <label>Weight (kg):</label>
    <input type="number" v-model="weight" placeholder="Enter your weight">

    <label>Height (cm):</label>
    <input type="number" v-model="height" placeholder="Enter your height">

    <label>Age:</label>
    <input type="number" v-model="age" placeholder="Enter your age">

    <h3>Daily Food Intake</h3>
    <div v-for="(food, index) in dailyFoodIntake" :key="index" class="food-item">
      <div class="food-search">
        <input
          type="text"
          v-model="food.food"
          placeholder="Food name"
          @input="filterFoodOptions(index)"
        />
        <ul v-if="filteredFoodOptions[index]?.length" class="dropdown">
          <li
            v-for="option in filteredFoodOptions[index]"
            :key="option"
            @click="selectFoodOption(index, option)"
          >
            {{ option }}
          </li>
        </ul>
      </div>
      <input type="number" v-model="food.weight" placeholder="Weight in grams" />
      <button @click="removeFood(index)">Remove</button>
    </div>
    <button @click="addFood">Add Food</button>

    <button @click="calculateWeightChange">Check Weight Status</button>

    <div v-if="result">
      <h3>Results</h3>
      <p><strong>Status:</strong> {{ result.status }}</p>
      <p><strong>BMR:</strong> {{ result.bmr }}</p>
      <p><strong>Total Calories Consumed:</strong> {{ result.total_calories }}</p>
      <p>{{ result.message }}</p>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";
import { useProfileStore } from "@/stores/profileStore"; // Import the profile store

export default {
  data() {
    return {
      gender: null,
      weight: null,
      height: null,
      age: null,
      dailyFoodIntake: [{ food: "", weight: null }],
      result: null,
      errorMessage: "",
      foodNames: [],
      filteredFoodOptions: [[]],
      showSuggestionsIndex: null,
    };
  },
  mounted() {
    axios.get("http://127.0.0.1:5000/food-names").then(response => {
      this.foodNames = response.data;
    });
    const profileStore = useProfileStore();
    this.gender = profileStore.gender;
    this.weight = profileStore.weight;
    this.height = profileStore.height;
    this.age = profileStore.age;
  },
  methods: {
    addFood() {
      this.dailyFoodIntake.push({ food: "", weight: null });
      this.filteredFoodOptions.push([]);
    },
    removeFood(index) {
      this.dailyFoodIntake.splice(index, 1);
    },
    async calculateWeightChange() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/weight-change", {
          gender: this.gender,
          weight: parseFloat(this.weight),
          height: parseFloat(this.height),
          age: parseInt(this.age),
          daily_food_intake: this.dailyFoodIntake,
        });

        this.result = response.data;
        this.errorMessage = "";
      } catch (error) {
        this.result = null;
        this.errorMessage =
          error.response?.data?.error || "Error checking weight change.";
      }
    },
    filterFoodOptions(index) {
      const input = this.dailyFoodIntake[index].food.toLowerCase();
      this.filteredFoodOptions[index] = this.foodNames.filter(name =>
        name.startsWith(input)
      ).slice(0, 5);
    },
    selectFoodOption(index, option) {
      this.dailyFoodIntake[index].food = option;
      this.filteredFoodOptions[index] = [];
      this.showSuggestionsIndex = null;
    },
    hideSuggestionsWithDelay() {
      setTimeout(() => {
        this.showSuggestionsIndex = null;
      }, 200);
    }
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #1e1e1e;
  color: #f0f0f0;
  border-radius: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2, h3 {
  margin-bottom: 1rem;
  color: #ffffff;
}

label {
  display: block;
  text-align: left;
  margin-top: 1rem;
  font-weight: 600;
}

input, select {
  width: 100%;
  padding: 10px;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 10px;
  border: none;
  font-size: 1rem;
}

input:focus, select:focus {
  outline: none;
  box-shadow: 0 0 5px #4caf50;
}

button {
  padding: 10px 16px;
  margin-top: 1rem;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  font-size: 1rem;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.food-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  gap: 10px;
}

.food-item input {
  width: 45%;
}

.error {
  margin-top: 1rem;
  color: #ff6b6b;
  font-weight: bold;
}

.dropdown {
  list-style: none;
  margin: 0;
  padding: 0;
  background-color: #333;
  border: 1px solid #555;
  border-radius: 10px;
  position: absolute;
  width: calc(100% - 20px);
  z-index: 1000;
  max-height: 150px;
  overflow-y: auto;
}

.dropdown li {
  padding: 10px;
  cursor: pointer;
  transition: background 0.2s;
}

.dropdown li:hover {
  background-color: #555;
}
</style>


