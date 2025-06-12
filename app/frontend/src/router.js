import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import JobList from './components/JobList.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld,
  },
  {
    path: '/viec-lam-it',
    name: 'Jobs',
    component: JobList,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;