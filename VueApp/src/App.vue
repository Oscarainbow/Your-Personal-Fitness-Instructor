<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
import { ref, provide, watch } from 'vue';
import { createPinia } from 'pinia';

import BmrCalculator from './components/BMRCalc.vue';
import WeightChangeCalc from './components/WeightChangeCalc.vue';
import ExercisePlan from './components/ExercisePlan.vue';
import LoginView from './views/LoginView.vue';
import ProfileView from './views/ProfileView.vue'; 

const router = useRouter();
const route = useRoute();
const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');

provide('isLoggedIn', isLoggedIn); // Provide `isLoggedIn` to all components

const logout = () => { // Logout function (also updates localStorage)
  isLoggedIn.value = false;
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('username');
  router.push('/login'); // Redirect to login
};

provide('logout', logout); // Provide logout globally

watch(route, () => { // Redirect unauthorized users from Profile
  if (route.path === '/profile' && !isLoggedIn.value) {
    router.push('/login');
  }
});



</script> 

<template>
  <div>
    <h1>Your Personal Fitness Instructor</h1>
    <p>Welcome to Y.P.F.I! This application consists of multiple features to help you track your weight, bmr, and calorie loss overtime.</p>
    <p>The application serves to be user-friendly and relatively simple to use, where all you have to do is enter the required information in the fields below, and the software can even generate a summary of calories lost given the diet and exercises you've done.</p>
    <p><strong>If you want your information to save, we suggest logging in. </strong></p>
  </div>
  <nav>

    <RouterLink to="/">Home</RouterLink> |
    <RouterLink to="/login">Login</RouterLink> |
    <RouterLink to="/exercises">Exercises</RouterLink> |
    <RouterLink to="/profile">Profile</RouterLink> |
    <button v-if="isLoggedIn" @click="logout">Logout</button>
    


  </nav>

 
  <LoginView v-if="showLogin" @closeLogin="toggleLogin" />

  <!-- Show these components only on the Home page -->
  <div v-if="$route.path === '/'">
      <h1>BMR Calculator</h1>
      <BmrCalculator />

      <h1>Weight Change Calculator</h1>
      <WeightChangeCalc /> 

      <h1>Your Plan</h1>
      <ExercisePlan />
    </div>

    <!-- This will load the Profile, Login, and other pages -->
    <RouterView :key="$route.fullPath" />


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
