import { createRouter, createWebHistory } from 'vue-router';
import JobList from './components/JobList.vue';
import JobDetail from './components/JobDetail.vue';
import ProcessCV from './components/FindJobCV.vue';
import CompanyDetail from './components/CompanyDetail.vue';
import HomePage from './components/HomePage.vue';

const routes = [
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
  {
    path: '/process_cv',
    name: 'ProcessCV',
    component: ProcessCV,
  },
  {
    path: '/company-detail',
    name: 'CompanyDetail',
    component: CompanyDetail,
  },
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;