<template>
  <div class="job-list">
    <div class="job-list-header">
      {{ totalJobs }} việc làm IT
    </div>
    <router-link
      v-for="job in jobs"
      :key="job.job_title"
      class="job-card"
      :to="{
        path: '/job-detail',
        query: {
          job_title: job.job_title,
          company_name: job.company_name
        }
      }"
      style="cursor:pointer; text-decoration: none; color: inherit;"
    >
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
            <span>
              {{ parseStringToArray(job.address)[0] }}
              <span v-if="parseStringToArray(job.employment_type)[0]">
                &nbsp;({{ parseStringToArray(job.employment_type)[0] }})
              </span>
            </span>
          </div>
        </div>
        <div class="tech-row">
          <div class="tech-list">
            <span
              v-for="tech in limitedTechs(job.technologies_used)"
              :key="tech"
              class="tech-badge"
            >{{ tech }}</span>
            <span
              v-if="isTechOverflow(job.technologies_used)"
              class="tech-ellipsis"
            >...</span>
          </div>
          <div class="date-posted">
            {{ parseStringToArray(job.date_posted)[0] }}
          </div>
        </div>
        <div class="bookmark-col">
          <svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import { parseStringToArray } from '../utils/parseStringToArray';

export default {
  name: 'JobCard',
  props: {
    jobs: {
      type: Array,
      required: true
    },
    totalJobs: {
      type: Number,
      required: true
    }
  },
  methods: {
    parseStringToArray,
    limitedTechs(techs) {
      const arr = this.parseStringToArray(techs);
      return arr.slice(0, 4);
    },
    isTechOverflow(techs) {
      const arr = this.parseStringToArray(techs);
      return arr.length > 4;
    },
  },
};
</script>

<style scoped>
.job-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
}
.job-list-header {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
  text-align: left;
}
.job-card {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  background: #f4faff;
  transition: background 0.2s, box-shadow 0.2s;
  border-radius: 12px;
  box-shadow: 0 2px 8px #0001;
  padding: 16px 20px 12px 20px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}
.job-card:hover {
  background: #e3f2fd;
  box-shadow: 0 4px 16px #0002;
}
.logo-col {
  flex: 0 0 80px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  margin-right: 24px;
}
.job-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
  background: #f8f8f8;
  border-radius: 10px;
}
.info-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding-right: 32px;
  position: relative;
}
.info-main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}
.job-title {
  font-size: 17px;
  font-weight: bold;
  color: #222;
  display: block;
  margin-bottom: 6px;
  text-align: left;
}
.company-name {
  font-size: 15px;
  color: #444;
  margin-bottom: 8px;
  text-align: left;
}
.meta-row {
  display: flex;
  align-items: center;
  font-size: 14px;
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
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
  text-align: left;
}
.tech-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  border-top: 2px solid #eee;
  padding-top: 8px;
  margin-top: 6px;
  width: 100%;
}
.tech-list {
  display: flex;
  gap: 4px;
  align-items: center;
}
.tech-badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
  margin-right: 2px;
  white-space: nowrap;
}
.tech-ellipsis {
  color: #1976d2;
  font-weight: bold;
  margin-left: 4px;
  font-size: 16px;
  background: none;
}
.date-posted {
  color: #888;
  font-size: 13px;
  text-align: right;
  margin-left: 8px;
  padding-right: 4px;
}
.bookmark-col {
  position: absolute;
  top: 0px;
  right: 0px;
  display: flex;
  align-items: flex-start;
}
.bookmark-col svg {
  width: 20px;
  height: 22px;
  stroke-width: 2;
}
</style>