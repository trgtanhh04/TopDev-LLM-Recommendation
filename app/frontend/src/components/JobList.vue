<template>
  <LoadingPage v-if="loading" />
  <div v-else class="job-list-layout">
    <div style="flex:1;">
      <JobCard :jobs="jobs" :total-jobs="totalJobs" />
      <div class="paging-controls">
        <button :disabled="page === 1" @click="handlePageChange(page - 1)">Previous</button>
        <span>Page {{ page }} of {{ totalPages }}</span>
        <button :disabled="page >= totalPages" @click="handlePageChange(page + 1)">Next</button>
      </div>
    </div>
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
      totalJobs: 0,
      page: 1,
      perPage: 15,
    };
  },
  computed: {
    totalPages() {
      return Math.max(1, Math.ceil(this.totalJobs / this.perPage));
    }
  },
  created() {
    // Set initial page from query or default to 1
    this.page = parseInt(this.$route.query.page) || 1;
    this.fetchJobs();
  },
  watch: {
    '$route.query.page'(newPage) {
      const pageNum = parseInt(newPage) || 1;
      if (pageNum !== this.page) {
        this.page = pageNum;
        this.fetchJobs();
      }
    }
  },
  methods: {
    async fetchJobs() {
      NProgress.start();
      this.loading = true;
      try {
        const res = await fetch(`${process.env.VUE_APP_API_URL}/jobs?page=${this.page}&perPage=${this.perPage}`);
        const data = await res.json();
        this.jobs = data.jobs;
        this.totalJobs = data.total_jobs;
        this.suggestedJobs = data.suggested_jobs;
      } catch (e) {
        console.error('Error loading jobs:', e);
      } finally {
        this.loading = false;
        NProgress.done();
      }
    },
    handlePageChange(newPage) {
      if (newPage < 1 || newPage > this.totalPages) return;
      // Update the URL query parameter
      this.$router.push({ 
        path: this.$route.path, 
        query: { ...this.$route.query, page: newPage } 
      });
    },
  }
};
</script>

<style scoped>
.job-list-layout {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 55px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  justify-content: center;
}
.paging-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 24px 0 32px 0;
  justify-content: center;
}
.paging-controls button {
  padding: 6px 16px;
  border-radius: 6px;
  border: 1px solid #1976d2;
  background: #fff;
  color: #1976d2;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
.paging-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>