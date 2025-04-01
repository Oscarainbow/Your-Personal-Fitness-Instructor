<script setup>
import { RouterLink, RouterView } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import BmrCalculator from './components/BMRCalc.vue';
import WeightChangeCalc from './components/WeightChangeCalc.vue';
import ExercisePlan from './components/ExercisePlan.vue';
import { ref } from 'vue';

const name = ref(''); // Reactive variable for input

</script>

<template>
  <div>
    <h1>Your Personal Fitness Instructor</h1>
    <p>Description of the application will go here</p>
  </div>
  <nav>
    <RouterLink to="/">Home</RouterLink> |
    <RouterLink to="/login">Login</RouterLink> |
    <RouterLink to="/exercises">Exercises</RouterLink>
  </nav>

  <RouterView />
 
  <LoginView v-if="showLogin" @closeLogin="toggleLogin" />


<div id="app">
  <h1>BMR Calculator</h1>
  <BmrCalculator />
</div>


<div id="app">
  <h1>Weight Change Calculator</h1>
  <WeightChangeCalc />
</div>

<div id="app">
  <h1>Your weight Loss</h1>
  <ExercisePlan />
</div>






</template>


<script>

  import { ref } from 'vue';
  import LoginView from './views/LoginView.vue';

  const showLogin = ref(false);

  const toggleLogin = () => {
    showLogin.value = !showLogin.value;
  };


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
