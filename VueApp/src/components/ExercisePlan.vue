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
        <div v-for="(food, index) in foodEntries" :key="index">
          <input v-model="food.food" placeholder="Food name" required />
          <input type="number" v-model.number="food.weight" placeholder="Weight (g)" required />
          <button @click.prevent="removeFood(index)">Remove</button>
        </div>
        <button @click.prevent="addFood">Add Food</button>
        
        <h3>Exercise</h3>
        <div v-for="(exercise, index) in exerciseEntries" :key="index">
          <input v-model="exercise.activity" placeholder="Exercise name" required />
          <input type="number" v-model.number="exercise.duration_mins" placeholder="Duration (mins)" required />
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
  import axios from 'axios';
  
  export default {
    data() {
      return {
        user_id: '',
        weight: '',
        height: '',
        age: '',
        gender: 'male',
        foodEntries: [],
        exerciseEntries: [],
        summary: null,
      };
    },
    methods: {
      addFood() {
        this.foodEntries.push({ food: '', weight: '' });
      },
      removeFood(index) {
        this.foodEntries.splice(index, 1);
      },
      addExercise() {
        this.exerciseEntries.push({ activity: '', duration_mins: '' });
      },
      removeExercise(index) {
        this.exerciseEntries.splice(index, 1);
      },
      async recordDaily() {
        try {
          await axios.post('http://localhost:5000/record-daily', {
            user_id: this.user_id,
            gender: this.gender,
            weight: this.weight,
            height: this.height,
            age: this.age,
            daily_food_intake: this.foodEntries,
            daily_exercise: this.exerciseEntries,
          });
          alert('Daily record saved successfully!');
        } catch (error) {
          alert('Error recording daily data');
        }
      },
      async getMonthlySummary() {
        try {
          const response = await axios.get('http://localhost:5000/monthly-summary', {
            params: { user_id: this.user_id, weight: this.weight }
          });
          this.summary = response.data;
        } catch (error) {
          alert('Error fetching summary');
        }
      }
    }
  };
  </script>
  
  <style>
  .container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  </style>
  
  