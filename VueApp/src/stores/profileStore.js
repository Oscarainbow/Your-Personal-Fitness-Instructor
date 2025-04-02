import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useProfileStore = defineStore('profile', {state: () => ({
    gender: localStorage.getItem('gender') || '',
    weight: localStorage.getItem('weight') || '',
    height: localStorage.getItem('height') || '',
    age: localStorage.getItem('age') || ''
  }),
  
  actions: {
    saveProfile({ gender, weight, height, age }) {
      this.gender = gender;
      this.weight = weight;
      this.height = height;
      this.age = age;

      // Save to localStorage so the data persists after page reload
      localStorage.setItem('gender', gender);
      localStorage.setItem('weight', weight);
      localStorage.setItem('height', height);
      localStorage.setItem('age', age);
    }
  }
});
