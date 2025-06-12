<template>
  <div class="job-list-layout">
    <JobCard />
    <JobSuggestion />
  </div>
</template>

<script>
import JobCard from './JobCard.vue';
import JobSuggestion from './JobSuggestion.vue';

export default {
  components: {
    JobCard,
    JobSuggestion,
  },
};
</script>

<style scoped>
.job-list-layout {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 70px;
  width: 100%;
  justify-content: center;
}
</style>