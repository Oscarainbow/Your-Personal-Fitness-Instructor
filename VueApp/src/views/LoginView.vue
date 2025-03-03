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

<script setup>
import { ref } from 'vue';

const username = ref('');
const password = ref('');
const isLoggedIn = ref(false);

const login = () => {
  if (username.value && password.value) {
    isLoggedIn.value = true;
  } else {
    alert('Please enter a valid username and password.');
  }
};

const logout = () => {
  isLoggedIn.value = false;
  username.value = '';
  password.value = '';
};
</script>

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
