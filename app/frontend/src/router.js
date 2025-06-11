import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import JobCard from './components/JobCard.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld,
  },
  {
    path: '/viec-lam-it',
    name: 'Jobs',
    component: JobCard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;