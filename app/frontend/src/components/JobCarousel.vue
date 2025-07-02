<template>
  <div class="job-carousel-section">
    <h2 class="section-title">Công việc đề xuất</h2>
    <div id="jobCarousel" class="carousel slide" data-ride="carousel" data-interval="5000">
      <div class="carousel-inner">
        <div
          v-for="(group, idx) in jobGroups"
          :key="idx"
          :class="['carousel-item', { active: idx === 0 }]"
        >
          <div class="row">
            <div
              v-for="job in group"
              :key="job.job_title + job.company_name"
              class="col-md-4"
            >
              <router-link
                class="job-card"
                :to="{
                  path: '/job-detail',
                  query: {
                    job_title: job.job_title,
                    company_name: job.company_name
                  }
                }"
              >
                <div class="logo-row">
                  <img
                    :src="parseStringToArray(job.small_image)[0]"
                    alt="Company Logo"
                    class="job-logo"
                  />
                  <span class="bookmark-icon">
                    <svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                    </svg>
                  </span>
                </div>
                <div class="job-title clamp-2">{{ job.job_title }}</div>
                <div class="company-name clamp-1">{{ job.company_name }}</div>
                <div class="meta-row">
                  <span class="salary" :class="{ highlight: job.salary === 'Negotiable' || job.salary === 'Thương lượng' }">{{ job.salary }}</span>
                </div>
                <div class="address-row">
                  {{ parseStringToArray(job.address)[0] }}
                </div>
                <div class="tech-row">
                  <div class="tech-list">
                    <span
                      v-for="tech in parseStringToArray(job.technologies_used)"
                      :key="tech"
                      class="tech-badge"
                    >{{ tech }}</span>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <a class="carousel-control-prev custom-arrow" href="#jobCarousel" role="button" data-slide="prev">
        <span class="carousel-arrow-icon" aria-hidden="true">&#8592;</span>
      </a>
      <a class="carousel-control-next custom-arrow" href="#jobCarousel" role="button" data-slide="next">
        <span class="carousel-arrow-icon" aria-hidden="true">&#8594;</span>
      </a>
    </div>
  </div>
</template>

<script>
import { parseStringToArray } from '../utils/parseStringToArray';

export default {
  name: 'JobCarousel',
  props: {
    jobs: {
      type: Array,
      required: true
    }
  },
  computed: {
    jobGroups() {
      const groups = [];
      for (let i = 0; i < this.jobs.length; i += 3) {
        groups.push(this.jobs.slice(i, i + 3));
      }
      return groups;
    },
  },
  methods: {
    parseStringToArray,
  },
  mounted() {
    this.$nextTick(() => {
      window.$('#jobCarousel').carousel({ interval: 5000, ride: 'carousel' });
    });
  },
  watch: {
    jobs() {
      this.$nextTick(() => {
        window.$('#jobCarousel').carousel({ interval: 5000, ride: 'carousel' });
      });
    }
  }
};
</script>

<style scoped>
.job-carousel-section {
  margin-top: 48px;
}
.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 18px;
}
.carousel-inner {
  width: 100%;
}
.job-card {
  display: block;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px #0001;
  padding: 18px 16px 16px 16px;
  margin: 12px 8px 24px 8px;
  min-height: 220px;
  position: relative;
  transition: box-shadow 0.18s, background 0.15s;
  text-decoration: none;
  color: inherit;
}
.job-card:hover {
  box-shadow: 0 4px 16px #1976d24c;
  background: #f4faff;
}
.logo-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 8px;
}
.job-logo {
  width: 60px;
  height: 36px;
  object-fit: contain;
  background: #f8f8f8;
  border-radius: 8px;
}
.bookmark-icon {
  margin-left: auto;
  margin-top: 2px;
}
.job-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #222;
  margin-bottom: 6px;
  text-align: left;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 2.6em;
}
.company-name {
  font-size: 1rem;
  font-weight: 500;
  color: #888;
  margin-bottom: 2px;
  text-align: left;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.meta-row {
  font-size: 1rem;
  color: #d32f2f;
  font-weight: 500;
  margin-bottom: 2px;
  text-align: left;
}
.salary.highlight {
  color: #d32f2f;
}
.address-row {
  font-size: 0.98rem;
  color: #222;
  margin-bottom: 8px;
  text-align: left;
}
.tech-row {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin-top: 6px;
  width: 100%;
}
.tech-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.tech-badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 10px;
  border-radius: 6px;
  font-size: 13px;
  margin-right: 2px;
  white-space: nowrap;
}
.carousel-arrow-icon {
  font-size: 2rem;
  color: #1976d2;
  display: flex;
  align-items: center;
  justify-content: center;
}
.custom-arrow {
  width: 36px;
  height: 36px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 1px 6px #0001;
  display: flex;
  align-items: center;
  justify-content: center;
  top: 40%;
  position: absolute;
  z-index: 2;
}
</style>