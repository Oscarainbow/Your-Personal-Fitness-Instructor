<template>
  <div class="profile-container">
    <h1>Your Profile</h1>
    <form @submit.prevent="saveProfile">
      <label for="gender">Gender:</label>
      <select id="gender" v-model="profile.gender">
        <option value="">Select</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
      </select>

      <label for="age">Age:</label>
      <input type="number" id="age" v-model="profile.age" min="1" />

      <label for="height">Height (cm):</label>
      <input type="number" id="height" v-model="profile.height" min="50" />

      <label for="weight">Weight (kg):</label>
      <input type="number" id="weight" v-model="profile.weight" min="20" />

      <button type="submit">Save Profile</button>
    </form>

    <div v-if="saved" class="profile-summary">
      <h2>Profile Summary</h2>
      <p><strong>Gender:</strong> {{ profile.gender }}</p>
      <p><strong>Age:</strong> {{ profile.age }}</p>
      <p><strong>Height:</strong> {{ profile.height }} cm</p>
      <p><strong>Weight:</strong> {{ profile.weight }} kg</p>
      <button @click="editProfile">Edit Profile</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const profile = ref({
  gender: '',
  age: '',
  height: '',
  weight: ''
});

const saved = ref(false);

const saveProfile = () => {
  saved.value = true;
};

const editProfile = () => {
  saved.value = false;
};
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-summary {
  margin-top: 20px;
  background-color: #f9f9f9;
  padding: 10px;
}

input,
select {
  margin-bottom: 10px;
}
</style>
