import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useProfileStore = defineStore('profile', {state: () => ({
    username: localStorage.getItem('username') || '',
    gender: localStorage.getItem('gender') || '',
    weight: localStorage.getItem('weight') || '',
    height: localStorage.getItem('height') || '',
    age: localStorage.getItem('age') || ''
  }),
  
  actions: {
    saveProfile({ username, gender, weight, height, age }) {
      this.username = username;
      this.gender = gender;
      this.weight = weight;
      this.height = height;
      this.age = age;

      //Save to localStorage so the data persists after page reload
      localStorage.setItem('username', username);
      localStorage.setItem('gender', gender);
      localStorage.setItem('weight', weight);
      localStorage.setItem('height', height);
      localStorage.setItem('age', age);
    }
  }
});
