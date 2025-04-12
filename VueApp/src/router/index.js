import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/LoginView.vue';
import ExercisesView from '../views/ExercisesView.vue';
import ProfileView from '../views/ProfileView.vue'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: Login },
    { path: '/exercises', component: ExercisesView },
    { path: '/profile', component: ProfileView }, 
  ],

})
export default router
