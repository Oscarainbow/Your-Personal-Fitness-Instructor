<template>
    <div class="container mt-5 text-center">
      <h3>BMR Calculator</h3>
      
      <div class="form-group">
        <label>Gender:</label>
        <input type="text" v-model="gender" class="form-control" placeholder="male or female" />
      </div>
  
      <div class="form-group">
        <label>Weight (kg):</label>
        <input type="number" v-model="weight" class="form-control" placeholder="Enter weight" />
      </div>
  
      <div class="form-group">
        <label>Height (cm):</label>
        <input type="number" v-model="height" class="form-control" placeholder="Enter height" />
      </div>
  
      <div class="form-group">
        <label>Age:</label>
        <input type="number" v-model="age" class="form-control" placeholder="Enter age" />
      </div>
  
      <button class="btn btn-primary mt-3" @click="calculateBmr">Calculate BMR </button>
  
      <div v-if="bmrResult" class="alert alert-success mt-3">
        <strong>Result:</strong> {{ bmrResult }}
      </div>
  
      <div v-if="error" class="alert alert-danger mt-3">
        <strong>Error:</strong> {{ error }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        gender: "",
        weight: "",
        height: "",
        age: "",
        bmrResult: "",  // shown in template
        error: ""       // shown in template
      };
    },

    methods: {
 
      async calculateBmr() {
        try {
          console.log("Sending request to backend...");
          const response = await axios.post("http://127.0.0.1:5000/bmr", {
            gender: this.gender,
            weight: parseFloat(this.weight),
            height: parseFloat(this.height),
            age: parseInt(this.age),
          });

          console.log("Response received:", response.data);
          this.bmrResult = `Your BMR is ${response.data.bmr} calories/day`;
          this.error = "";
        } catch (error) {
          console.error("Axios Error:", error.response ? error.response.data : error.message);
          this.error = "Failed to calculate BMR. Please check input values.";
          this.bmrResult = "";
        }
      }

    }
  };    
  </script>
  
  <style>
  .container {
    max-width: 600px;
    margin: auto;
  }
  .form-group {
    margin-bottom: 10px;
  }
  </style>
  