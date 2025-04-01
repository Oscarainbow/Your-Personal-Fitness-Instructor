<template>
    <div>
      <h1>Exercise List</h1>
      <ol>
       <!-- <li v-for="exercise in exercises" :key="exercise.id">
          {{ exercise.name }}
        </li> -->

        <li>Cardio Exercises</li>
          <ul>
            <li>Jogging</li>              
              <h2>Recommended Jogging Duration</h2>
              <table>
                <tr>
                  <th>Fitness Level</th>
                  <th>Duration</th>
                  <th>Frequency</th>
                </tr>
                <tr>
                  <td>Beginners</td>
                  <td>15-20 minutes</td>
                  <td>3-4 times a week</td>
                </tr>
                <tr>
                  <td>Intermediate</td>
                  <td>30-40 minutes</td>
                  <td>4-5 times a week</td>
                </tr>
                <tr>
                  <td>Advanced</td>
                  <td>45+ minutes</td>
                  <td>5+ times a week</td>
                </tr>
              </table>
            
          <!-- <p>Recommended Jogging Duration: 
              Beginners: 15-20 minutes, 3-4 times a week. 
              Intermediate: 30-40 minutes, 4-5 times a week. 
              Advanced: 45+ minutes, 5+ times a week.</p> -->


            <li>Jumping Jacks</li>
            <li>Burpee</li>
            <li>Jump-Rope</li>
            <li>Cycling</li>
          </ul>
        
        <li>Strength Training</li>
          <ul>
            <li>Push-Ups</li>
            <li>Pull-Ups</li>
            <li>Squats</li>
            <li>Sit-Ups</li>
            <li>Plank</li>      
          </ul>

      </ol>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const exercises = ref([
    { id: 1, name: "Push-ups" },
    { id: 2, name: "Squats" },
    { id: 3, name: "Plank" },
    { id: 4, name: "Jumping Jacks" },
  ]);
  </script>
  