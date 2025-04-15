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
  margin: 2rem auto;
  padding: 2rem;
  background-color: #1e1e1e;
  color: #f0f0f0;
  border-radius: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

h3 {
  margin-bottom: 1.5rem;
  color: #ffffff;
}

.form-group {
  text-align: left;
  margin-bottom: 1.2rem;
}

label {
  font-weight: 600;
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  border: none;
  font-size: 1rem;
  background-color: #2a2a2a;
  color: #f0f0f0;
}

input:focus {
  outline: none;
  box-shadow: 0 0 5px #4caf50;
}

.btn {
  padding: 10px 20px;
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

.btn:hover {
  background-color: #45a049;
}

.alert {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 10px;
  font-weight: bold;
}

.success {
  background-color: #2e7d32;
  color: #c8fdd9;
}

.error {
  background-color: #b71c1c;
  color: #ffbdbd;
}
  </style>
  