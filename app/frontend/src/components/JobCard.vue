<template>
  <div class="job-list">
    <div v-for="job in jobs" :key="job.job_title" class="job-card">
      <div class="logo-col">
        <img :src="parseStringToArray(job.small_image)[0]" alt="Company Logo" class="job-logo" />
      </div>
      <div class="info-col">
        <div class="info-main">
          <span class="job-title">{{ job.job_title }}</span>
          <div class="company-name">{{ job.company_name }}</div>
          <div class="meta-row">
            <span class="salary" :class="{ highlight: job.salary === 'Thương lượng' }">{{ job.salary }}</span>
            <span class="dot">•</span>
            <span class="position-level">{{ parseStringToArray(job.position_level).join(', ') }}</span>
          </div>
          <div class="address-row">
            <span>{{ parseStringToArray(job.address)[0] }}</span>
            <span v-if="parseStringToArray(job.employment_type)[0]">({{ parseStringToArray(job.employment_type)[0] }})</span>
          </div>
        </div>
        <div class="tech-row">
          <div class="tech-list">
            <span v-for="tech in parseStringToArray(job.technologies_used)" :key="tech" class="tech-badge">{{ tech }}</span>
          </div>
          <div class="date-posted">
            {{ parseStringToArray(job.date_posted)[0] }}
          </div>
        </div>
        <div class="bookmark-col">
          <svg width="24" height="24" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { parseStringToArray } from '../utils/parseStringToArray';

export default {
  name: 'JobCard',
  data() {
    return {
      jobs: [],
    };
  },
  async created() {
    try {
      const response = await fetch(`${process.env.VUE_APP_API_URL}/jobs?page=1&perPage=10`, {
        headers: {
          accept: 'application/json',
        },
      });
      const data = await response.json();
      this.jobs = data.jobs;
    } catch (error) {
      console.error('Error fetching jobs:', error);
    }
  },
  methods: {
    parseStringToArray,
  },
};
</script>

<style scoped>
.job-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
}
.job-card {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px #0001;
  padding: 32px 32px 24px 32px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}
.logo-col {
  flex: 0 0 120px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  margin-right: 32px;
}
.job-logo {
  width: 100px;
  height: 100px;
  object-fit: contain;
  background: #f8f8f8;
  border-radius: 12px;
}
.info-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  position: relative;
  padding-right: 48px;
}
.info-main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}
.job-title {
  font-size: 24px;
  font-weight: bold;
  color: #222;
  display: block;
  margin-bottom: 4px;
  text-align: left;
}
.company-name {
  font-size: 16px;
  color: #444;
  margin-bottom: 8px;
  text-align: left;
}
.meta-row {
  display: flex;
  align-items: center;
  font-size: 15px;
  color: #222;
  margin-bottom: 4px;
  text-align: left;
}
.salary {
  color: #d32f2f;
  font-weight: 500;
}
.salary.highlight {
  color: #d32f2f;
}
.dot {
  margin: 0 8px;
  color: #888;
}
.position-level {
  color: #222;
}
.address-row {
  font-size: 15px;
  color: #555;
  margin-bottom: 8px;
  text-align: left;
}
.tech-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
  padding-top: 12px;
  margin-top: 8px;
  width: 100%;
}
.tech-list {
  display: flex;
  gap: 8px;
}
.tech-badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 6px 18px;
  border-radius: 8px;
  font-size: 16px;
  margin-right: 8px;
  white-space: nowrap;
}
.date-posted {
  color: #888;
  font-size: 16px;
  min-width: 120px;
  text-align: right;
  margin-left: auto;
}
.bookmark-col {
  position: absolute;
  right: 32px;
  top: 32px;
  cursor: pointer;
}
</style>