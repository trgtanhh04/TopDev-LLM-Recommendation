<template>
  <div class="home-page">
    <div class="search-bar">
      <input
        v-model="keyword"
        @keyup.enter="fetchSuggestions"
        type="text"
        placeholder="Tìm kiếm công việc hoặc công ty theo từ khóa (Ví dụ: BIDV, Network, ...)"
      />
      <button @click="fetchSuggestions">Tìm kiếm</button>
    </div>
    <LoadingPage v-if="loading" />
    <template v-else>
      <CompanyCarousel :companies="companies" />
      <JobCarousel :jobs="jobs" />
    </template>
  </div>
</template>

<script>
import CompanyCarousel from './CompanyCarousel.vue';
import JobCarousel from './JobCarousel.vue';
import LoadingPage from './LoadingPage.vue';

export default {
  name: 'HomePage',
  components: { CompanyCarousel, JobCarousel, LoadingPage },
  data() {
    return {
      companies: [],
      jobs: [],
      loading: true,
      keyword: '',
    };
  },
  async created() {
    await this.fetchSuggestions();
  },
  methods: {
    async fetchSuggestions() {
      this.loading = true;
      try {
        const params = new URLSearchParams();
        params.append('perPage', 24);
        if (this.keyword.trim()) {
          params.append('keyword', this.keyword.trim());
        }
        const res = await fetch(`${process.env.VUE_APP_API_URL}/suggested-home?${params.toString()}`);
        const data = await res.json();
        this.companies = data.suggested_companies;
        this.jobs = data.suggested_jobs;
      } catch (e) {
        this.companies = [];
        this.jobs = [];
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.home-page {
  max-width: 1300px;
  margin: 0 auto;
  padding: 32px 0;
}
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  width: 100%;
}
.search-bar input {
  flex: 1;
  min-width: 0;
  width: 0;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #1976d2;
  font-size: 1.1rem;
}
.search-bar button {
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 22px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.18s;
}
.search-bar button:hover {
  background: #0d47a1;
}
</style>