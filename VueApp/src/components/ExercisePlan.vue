<template>
  <div class="container">
    <h1>Weight Loss Tracker</h1>
    <form @submit.prevent="recordDaily">
      <label>User ID:</label>
      <input v-model="user_id" required />

      <label>Weight (kg):</label>
      <input type="number" v-model.number="weight" required />

      <label>Height (cm):</label>
      <input type="number" v-model.number="height" required />

      <label>Age:</label>
      <input type="number" v-model.number="age" required />

      <label>Gender:</label>
      <select v-model="gender">
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>

      <h3>Food Intake</h3>
      <div v-for="(food, index) in foodEntries" :key="'food-' + index" class="autocomplete-entry">
        <div class="autocomplete">
          <input
            v-model="food.food"
            placeholder="Food name"
            @input="filterFoodSuggestions(index)"
            @blur="hideFoodSuggestions(index)"
            @focus="filterFoodSuggestions(index)"
            required
          />
          <ul v-if="filteredFoodSuggestions[index]?.length" class="suggestions">
            <li
              v-for="option in filteredFoodSuggestions[index]"
              :key="option"
              @click="selectFoodSuggestion(index, option)"
            >
              {{ option }}
            </li>
          </ul>
        </div>
        <input type="number" v-model.number="food.weight" placeholder="Weight (g)" required />
        <button @click.prevent="removeFood(index)">Remove</button>
      </div>
      <button @click.prevent="addFood">Add Food</button>

      <h3>Exercise</h3>
      <div v-for="(exercise, index) in exerciseEntries" :key="'exercise-' + index" class="autocomplete-entry">
        <div class="autocomplete">
          <input
            v-model="exercise.activity"
            placeholder="Exercise name"
            @input="filterExerciseSuggestions(index)"
            @blur="hideExerciseSuggestions(index)"
            @focus="filterExerciseSuggestions(index)"
            required
          />
          <ul v-if="filteredExerciseSuggestions[index]?.length" class="suggestions">
            <li
              v-for="option in filteredExerciseSuggestions[index]"
              :key="option"
              @click="selectExerciseSuggestion(index, option)"
            >
              {{ option }}
            </li>
          </ul>
        </div>
        <input
          type="number"
          v-model.number="exercise.duration_mins"
          placeholder="Duration (mins)"
          required
        />
        <button @click.prevent="removeExercise(index)">Remove</button>
      </div>
      <button @click.prevent="addExercise">Add Exercise</button>

      <button type="submit">Record Daily Data</button>
    </form>

    <button @click="getMonthlySummary">Get Monthly Summary</button>
    <div v-if="summary">
      <h2>Monthly Summary</h2>
      <p>Total Calories In: {{ summary.total_calories_in }}</p>
      <p>Total Calories Out: {{ summary.total_calories_out }}</p>
      <p>Net Deficit: {{ summary.net_deficit }}</p>
      <p>Estimated Weight Change: {{ summary.estimated_weight_change_kg }} kg</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useProfileStore } from "@/stores/profileStore";

export default {
  data() {
    const profileStore = useProfileStore();
    return {
      user_id: profileStore.username,
      weight: profileStore.weight,
      height: profileStore.height,
      age: profileStore.age,
      gender: profileStore.gender,
      foodEntries: [],
      exerciseEntries: [],
      foodSuggestions: [],
      exerciseSuggestions: [],
      filteredFoodSuggestions: [],
      filteredExerciseSuggestions: [],
      summary: null,
    };
  },
  
  mounted() {
    console.log("Component mounted");
    axios.get("http://127.0.0.1:5000/food-names").then((res) => {
      this.foodSuggestions = res.data;
      console.log("Fetched food suggestions:", this.foodSuggestions);
    });
    axios.get("http://127.0.0.1:5000/exercise-names").then((res) => {
      this.exerciseSuggestions = res.data;
      console.log("Fetched exercise suggestions:", this.exerciseSuggestions);
    });
  },
  methods: {
    addFood() {
      this.foodEntries.push({ food: "", weight: "" });
      this.filteredFoodSuggestions.push([]);
    },
    removeFood(index) {
      this.foodEntries.splice(index, 1);
      this.filteredFoodSuggestions.splice(index, 1);
    },
    addExercise() {
      this.exerciseEntries.push({ activity: "", duration_mins: "" });
      this.filteredExerciseSuggestions.push([]);
    },
    removeExercise(index) {
      this.exerciseEntries.splice(index, 1);
      this.filteredExerciseSuggestions.splice(index, 1);
    },
    async recordDaily() {
      try {
        await axios.post("http://localhost:5000/record-daily", {
          user_id: this.user_id,
          gender: this.gender,
          weight: this.weight,
          height: this.height,
          age: this.age,
          daily_food_intake: this.foodEntries,
          daily_exercise: this.exerciseEntries,
        });
        alert("Daily record saved successfully!");
      } catch (error) {
        alert("Error recording daily data");
      }
    },
    async getMonthlySummary() {
      try {
        const response = await axios.get("http://localhost:5000/monthly-summary", {
          params: { user_id: this.user_id, weight: this.weight },
        });
        this.summary = response.data;
      } catch (error) {
        alert("Error fetching summary");
      }
    },
    filterFoodSuggestions(index) {
      const input = this.foodEntries[index].food.toLowerCase();
      this.filteredFoodSuggestions[index] = this.foodSuggestions
        .filter((item) => item.toLowerCase().startsWith(input))
        .slice(0, 5);
    },
    selectFoodSuggestion(index, option) {
      this.foodEntries[index].food = option;
      this.filteredFoodSuggestions[index] = [];
    },
    hideFoodSuggestions(index) {
      setTimeout(() => {
        this.filteredFoodSuggestions[index] = [];
      }, 200);
    },
    filterExerciseSuggestions(index) {
      const input = this.exerciseEntries[index].activity.toLowerCase();
      this.filteredExerciseSuggestions[index] = this.exerciseSuggestions
        .filter((item) => item.toLowerCase().startsWith(input))
        .slice(0, 5);
    },
    selectExerciseSuggestion(index, option) {
      this.exerciseEntries[index].activity = option;
      this.filteredExerciseSuggestions[index] = [];
    },
    hideExerciseSuggestions(index) {
      setTimeout(() => {
        this.filteredExerciseSuggestions[index] = [];
      }, 200);
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

input, select {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}

button {
  margin: 5px 0;
  padding: 8px 12px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.autocomplete {
  position: relative;
}

.suggestions {
  position: absolute;
  z-index: 1000;
  background: black;
  border: 1px solid #ccc;
  width: 100%;
  list-style: none;
  padding: 0;
  margin-top: 0;
  max-height: 150px;
  overflow-y: auto;
}

.suggestions li {
  padding: 8px;
  cursor: pointer;
}

.suggestions li:hover {
  background-color: #f0f0f0;
}

.autocomplete-entry {
  margin-bottom: 10px;
}
</style>

  
  