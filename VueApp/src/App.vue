<script setup>
import { RouterLink, RouterView } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import BmrCalculator from './components/BMRCalc.vue';
import WeightChangeCalc from './components/WeightChangeCalc.vue';
import { ref } from 'vue';

const name = ref(''); // Reactive variable for input

</script>

<template>
  <div>
    <h1>Your Personal Fitness Instructor</h1>
    <p>Description of the application will go here</p>
  </div>
  
 

    <div> <!-- class="container text-center mt-5" -->
      
      <h4>Test textbox</h4>
      <input type="text" v-model="name" placeholder="Type Name Here" />
      <p>You entered: {{ name }}</p>
     
     
      <div class="container mt-5 text-center">
        <h3>Enter Text:</h3>
        <input type="text" v-model="userInput" class="form-control my-2" placeholder="Type something..." />
  
        <button class="btn btn-primary" @click="submitText"> Submit </button>

        <div v-if="processedText" class="alert alert-success mt-3">
          <strong>Processed Text:</strong> {{ processedText }}
        </div>

        <div v-if="error" class="alert alert-danger mt-3">
          <strong>Error:</strong> {{ error }}
        </div>
      </div>
    </div>

<div>
  <nav>
    <RouterLink to="/login">Go to Login Page</RouterLink>
    <RouterView />
  </nav>
</div>



<div id="app">
  <h1>BMR Calculator</h1>
  <BmrCalculator />
</div>


<div id="app">
  <h1>Weight Change Calculator</h1>
  <WeightChangeCalc />
</div>

</template>


<script>

export default {
  
  data() {
    return {
      userInput: '', //Stores input text
      processedText: '', //Stores processed text from Python
      error: '' //Stores error messages
    };
  },
  methods: {
    async submitText() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/submit-text', {
          text: this.userInput
        });
        this.processedText = response.data.processed_text; //Store processed text
        this.error = ''; //Clear any previous errors
      } catch (err) {
        this.error = 'Failed to process input'; //Handle errors
      }
    }
  }
};

</script>




<style scoped>
h1 {
    margin: auto;
    text-align: center;
}
</style>
