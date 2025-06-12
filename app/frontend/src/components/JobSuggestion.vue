<template>
  <div class="job-suggestion-container">
    <div class="header">Có thể bạn sẽ thích</div>
    <div v-for="(job, idx) in suggestedJobs" :key="idx" class="job-suggestion-card">
      <div class="logo">
        <img :src="parseStringToArray(job.small_image)[0]" alt="logo" />
      </div>
      <div class="info">
        <div class="job-title">{{ job.job_title }}</div>
        <div class="company">{{ job.company_name }}</div>
        <div v-if="parseStringToArray(job.technologies_used).length" class="tags">
          <span
            v-for="tag in limitedTechs(job.technologies_used)"
            :key="tag"
            class="tag"
          >{{ tag }}</span>
          <span
            v-if="isTechOverflow(job.technologies_used)"
            class="tag ellipsis"
          >...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { parseStringToArray } from '../utils/parseStringToArray';

export default {
  name: 'JobSuggestion',
  props: {
    suggestedJobs: {
      type: Array,
      required: true
    }
  },
  methods: {
    parseStringToArray,
    limitedTechs(techs) {
      const arr = this.parseStringToArray(techs);
      return arr.slice(0, 2);
    },
    isTechOverflow(techs) {
      const arr = this.parseStringToArray(techs);
      return arr.length > 2;
    },
  },
};
</script>

<style scoped>
.job-suggestion-container {
  background: #f4faff;
  border-radius: 8px;
  box-shadow: 0 1px 6px #0001;
  width: 360px;
  border: 1px solid #eee;
  font-family: Arial, sans-serif;
  padding: 0;
}
.header {
  font-weight: bold;
  font-size: 18px;
  padding: 16px 16px 12px 16px;
  border-bottom: 1px solid #eee;
  background: #e3f2fd;
  text-align: left;
}
.job-suggestion-card {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-bottom: 1px solid #eee;
  gap: 12px;
  background: #f4faff;
}
.job-suggestion-card:last-child {
  border-bottom: none;
}
.logo img {
  width: 50px;
  height: 50px;
  object-fit: contain;
  border-radius: 6px;
  background: #f8f8f8;
  margin-right: 10px;
}
.info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.job-title {
  font-weight: bold;
  font-size: 16px;
  color: #222;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
  max-width: 250px;
}
.company {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
  max-width: 250px;
}
.tags {
  margin-top: 4px;
  display: flex;
  gap: 6px;
}
.tag {
  background: #e3f2fd;
  color: #1976d2;
  font-size: 13px;
  padding: 2px 10px;
  border-radius: 6px;
  white-space: nowrap;
}
.ellipsis {
  font-weight: bold;
  background: none;
  color: #1976d2;
  font-size: 16px;
  padding: 0 4px;
}
</style>