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
  max-width: 500px;
  margin: auto;
  text-align: center;
}
input, select {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
button {
  padding: 8px;
  margin: 5px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
.error {
  color: red;
}
.food-item {
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
}
.food-item input {
  width: 45%;
}
.autocomplete {
  position: relative;
}
.suggestions {
  position: absolute;
  background: black;
  border: 1px solid #ccc;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 10;
}
.suggestions li {
  padding: 8px;
  cursor: pointer;
}
.suggestions li:hover {
  background-color: #f0f0f0;
}
</style>


