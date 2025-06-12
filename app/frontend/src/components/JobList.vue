<template>
  <LoadingPage v-if="loading" />
  <div v-else class="job-list-layout">
    <JobCard :jobs="jobs" />
    <JobSuggestion :suggestedJobs="suggestedJobs" />
  </div>
</template>

<script>
import JobCard from './JobCard.vue';
import JobSuggestion from './JobSuggestion.vue';
import LoadingPage from './LoadingPage.vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

export default {
  components: { JobCard, JobSuggestion, LoadingPage },
  data() {
    return {
      jobs: [],
      suggestedJobs: [],
      loading: true,
    };
  },
  async created() {
    NProgress.start();
    try {
      const [jobsRes, suggestedRes] = await Promise.all([
        fetch(`${process.env.VUE_APP_API_URL}/jobs?page=1&perPage=10`),
        fetch(`${process.env.VUE_APP_API_URL}/suggested-jobs?perPage=5`)
      ]);
      const jobsData = await jobsRes.json();
      const suggestedData = await suggestedRes.json();
      this.jobs = jobsData.jobs;
      this.suggestedJobs = suggestedData['suggested-jobs'];
    } catch (e) {
      console.error('Error loading jobs:', e);
    } finally {
      this.loading = false;
      NProgress.done();
    }
  }
};
</script>

<style scoped>
.job-list-layout {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 32px;
  width: 100%;
  justify-content: center;
}
.loading-area {
  width: 100%;
  text-align: center;
  padding: 48px 0;
  font-size: 20px;
  color: #1976d2;
}
</style>