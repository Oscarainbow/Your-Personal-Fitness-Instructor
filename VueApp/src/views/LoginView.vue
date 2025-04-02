<script setup>
import { ref, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const isLoggedIn = inject('isLoggedIn'); // Use global state
const logout = inject('logout'); // Inject global logout function

// On mounted, check if logged in and load the username if available
onMounted(() => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
  if (isLoggedIn.value) {
    username.value = localStorage.getItem('username') || ''; // Get username from localStorage
  }
});

const login = () => {
  if (username.value && password.value) {
    isLoggedIn.value = true;
    localStorage.setItem('isLoggedIn', 'true'); // Store login state
    localStorage.setItem('username', username.value); // Store username in localStorage
    router.push('/profile'); // Redirect to profile page
  } else {
    alert('Please enter a valid username and password.');
  }
};

</script>

<template>
  <div class="login-container">
    <h2 v-if="!isLoggedIn">Login</h2>

    <div v-if="!isLoggedIn">
      <input type="text" v-model="username" placeholder="Enter username" />
      <input type="password" v-model="password" placeholder="Enter password" />
      <button @click="login">Login</button>
    </div>

    <div v-else>
      <h2>Welcome, {{ username }}!</h2>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 300px;
    margin: auto;
  }
  input, button {
    padding: 8px;
    font-size: 16px;
  }
</style>
