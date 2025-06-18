import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import JobList from './components/JobList.vue';
import JobDetail from './components/JobDetail.vue';

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
  {
    path: '/job-detail',
    name: 'JobDetail',
    component: JobDetail,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;