<template>
  <div class="profile-container">
    <h1>Your Profile</h1>

    <form v-if="!saved" @submit.prevent="saveProfile">
      <label for="gender">Gender:</label>
      <select id="gender" v-model="store.gender">
        <option value="">Select</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
      </select>

      <label for="age">Age:</label>
      <input type="number" id="age" v-model="store.age" min="1" />

      <label for="height">Height (cm):</label>
      <input type="number" id="height" v-model="store.height" min="50" />

      <label for="weight">Weight (kg):</label>
      <input type="number" id="weight" v-model="store.weight" min="20" />

      <button type="submit">Save Profile</button>
    </form>

    <div v-if="saved" class="profile-summary">
      <h2>Profile Summary</h2>
      <p><strong>Username:</strong> {{ store.username }}</p>
      <p><strong>Gender:</strong> {{ store.gender }}</p>
      <p><strong>Age:</strong> {{ store.age }}</p>
      <p><strong>Height:</strong> {{ store.height }} cm</p>
      <p><strong>Weight:</strong> {{ store.weight }} kg</p>
      <button @click="editProfile">Edit Profile</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useProfileStore } from '@/stores/profileStore';

const store = useProfileStore();
const saved = ref(false);

onMounted(() => {
  if (store.username && store.gender && store.age && store.height && store.weight) {
    saved.value = true;
  }
});

const saveProfile = () => {
  store.saveProfile({
    username: store.username,
    gender: store.gender,
    age: store.age,
    height: store.height,
    weight: store.weight
  });
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
