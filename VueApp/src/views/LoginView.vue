<template>
    <div class="login-container">
      <h2>Login</h2>
      <input type="text" v-model="username" placeholder="Enter username" />
      <input type="password" v-model="password" placeholder="Enter password" />
      <button @click="login">Login</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const username = ref('');
  const password = ref('');
  
  const login = () => {
    alert(`Logging in as: ${username.value}`);
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
  