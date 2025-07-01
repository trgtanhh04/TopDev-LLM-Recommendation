<template>
  <div class="home-page">
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
    };
  },
  async created() {
    this.loading = true;
    try {
      const res = await fetch(`${process.env.VUE_APP_API_URL}/suggested-home?perPage=24`);
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
};
</script>

<style scoped>
.home-page {
  max-width: 1300px;
  margin: 0 auto;
  padding: 32px 0;
}
</style>