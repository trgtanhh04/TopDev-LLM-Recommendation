<template>
  <div v-if="loading">
    <LoadingPage />
  </div>
  <div v-else-if="companyDetail" class="company-detail-card">
    <!-- Banner -->
    <div v-if="bigImage" class="banner">
      <img :src="bigImage" alt="Banner" />
    </div>
    <!-- Main Info Card -->
    <div class="main-info-card">
      <img class="company-logo" :src="smallImage" alt="Logo" v-if="smallImage" />
      <div class="main-info">
        <div class="company-name">{{ companyDetail.name }}</div>
        <div class="company-tagline">{{ companyDetail.tag_line }}</div>
        <div class="job-opening-row" v-if="companyDetail.opening_jobs">
          <span>
            <svg width="18" height="18" fill="none" viewBox="0 0 22 22"><circle cx="11" cy="11" r="9" fill="#e3f2fd"/><circle cx="11" cy="11" r="8" stroke="#bfc8e6" stroke-width="1.5"/><rect x="10.25" y="6.5" width="1.5" height="5" rx="0.75" fill="#bfc8e6"/><rect x="11" y="11" width="4" height="1.5" rx="0.75" transform="rotate(45 11 11)" fill="#bfc8e6"/></svg>
            {{ companyDetail.opening_jobs }} jobs opening
          </span>
        </div>
      </div>
    </div>

    <!-- Meta Info Section -->
    <div class="company-meta-row">
      <div class="info-company-block">
        <div class="info-icon">🏷️</div>
        <div>
          <div class="info-label">Industry</div>
          <div class="info-value">{{ parseStringToArray(companyDetail.industry)[0] }}</div>
        </div>
      </div>
      <div class="info-company-block">
        <div class="info-icon">👥</div>
        <div>
          <div class="info-label">Company size</div>
          <div class="info-value">{{ parseStringToArray(companyDetail.company_size).join(', ') }}</div>
        </div>
      </div>
      <div class="info-company-block">
        <div class="info-icon">🏳️</div>
        <div>
          <div class="info-label">Nationality</div>
          <div class="info-value">{{ parseStringToArray(companyDetail.nationality).join(', ') }}</div>
        </div>
      </div>
    </div>
    <div class="company-meta-row single">
      <div class="info-company-block">
        <div class="info-icon">💻</div>
        <div>
          <div class="info-label">Tech stack</div>
          <div class="info-value">
            <span v-for="tech in parseStringToArray(companyDetail.tech_stack)" :key="tech" class="tech-tag">{{ tech }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="company-meta-row single">
      <div class="info-company-block">
        <div class="info-icon">🌐</div>
        <div>
          <div class="info-label">Website</div>
          <div class="info-value">
            <span v-for="(web, idx) in parseStringToArray(companyDetail.website)" :key="web">
              <a :href="web" target="_blank" rel="noopener">{{ web }}</a>
              <span v-if="idx < parseStringToArray(companyDetail.website).length - 1">, </span>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="company-meta-row single">
      <div class="info-company-block">
        <div class="info-icon">📍</div>
        <div>
          <div class="info-label">Office address</div>
          <div class="info-value">
            <span v-for="(addr, idx) in parseStringToArray(companyDetail.office_address)" :key="addr">
              {{ addr }}<span v-if="idx < parseStringToArray(companyDetail.office_address).length - 1">, </span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Company profile sections -->
    <div class="company-profile-block">
      <div v-for="section in profileSections" :key="section.header" class="company-profile-section">
        <h4 class="profile-header">{{ section.header }}</h4>
        <div class="profile-content">
          {{ section.content }}
        </div>
      </div>
    </div>

    <!-- Gallery -->
    <div v-if="galleryImages.length" class="gallery">
      <img v-for="img in galleryImages" :src="img" :key="img" class="gallery-img" />
    </div>
  </div>
  <div v-else>
    Không tìm thấy thông tin công ty.
  </div>
</template>

<script>
import LoadingPage from './LoadingPage.vue';
import { parseStringToArray } from '../utils/parseStringToArray';
import { parseCompanyProfileToSections } from '../utils/parseCompanyProfileSections';

export default {
  components: { LoadingPage },
  data() {
    return {
      companyDetail: null,
      loading: true,
    };
  },
  computed: {
    smallImage() {
      if (!this.companyDetail) return '';
      const arr = parseStringToArray(this.companyDetail.small_image);
      return arr.length ? arr[0] : '';
    },
    bigImage() {
      if (!this.companyDetail) return '';
      const arr = parseStringToArray(this.companyDetail.big_image);
      return arr.length ? arr[0] : '';
    },
    galleryImages() {
      if (!this.companyDetail) return [];
      return parseStringToArray(this.companyDetail.image_galleries).filter(img => img && img.trim());
    },
    profileSections() {
      if (!this.companyDetail) return [];
      return parseCompanyProfileToSections(this.companyDetail.company_profile);
    }
  },
  methods: {
    parseStringToArray,
    async loadCompanyDetail() {
      const { company_name } = this.$route.query;
      if (!company_name) {
        this.loading = false;
        return;
      }
      try {
        const url = `${process.env.VUE_APP_API_URL}/company-detail?company_name=${encodeURIComponent(company_name)}`;
        const res = await fetch(url);
        const data = await res.json();
        this.companyDetail = data.company_detail;
      } catch (e) {
        this.companyDetail = null;
      } finally {
        this.loading = false;
      }
    }
  },
  created() {
    this.loadCompanyDetail();
  }
};
</script>

<style scoped>
.company-detail-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #0001;
  padding: 0 0 18px 0;
  max-width: 1200px;
  margin: 32px auto;
  font-family: Arial, sans-serif;
}
.banner img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 12px 12px 0 0;
}
.main-info-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px 32px 0 32px;
}
.company-logo {
  width: 90px;
  height: 90px;
  object-fit: contain;
  border-radius: 10px;
  background: #f8f8f8;
}
.main-info {
  flex: 1;
}
.company-name {
  color: #ff5a36;
  font-weight: bold;
  font-size: 26px;
  margin-bottom: 4px;
}
.company-tagline {
  color: #444;
  font-size: 16px;
  margin-bottom: 8px;
}
.job-opening-row {
  color: #1976d2;
  font-size: 15px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.company-meta-row {
  display: flex;
  gap: 200px;
  margin: 32px 0 0 0;
  padding: 0 32px;
  flex-wrap: wrap;
}
.company-meta-row.single {
  gap: 0;
  margin-top: 24px;
}
.info-company-block {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  min-width: 220px;
}
.info-icon {
  font-size: 22px;
  margin-right: 6px;
  flex-shrink: 0;
}
.info-label {
  font-size: 14px;
  color: #888;
  margin-bottom: 2px;
}
.info-value {
  font-size: 16px;
  font-weight: bold;
  color: #222;
}
.tech-tag {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 6px;
  padding: 2px 8px;
  margin-right: 6px;
  font-size: 13px;
  display: inline-block;
}
.company-profile-block {
  margin: 36px 32px 36px 32px;
}
.profile-header {
  margin-bottom: 6px;
  color: #d32f2f;
  font-size: 18px;
  font-weight: bold;
}
.profile-content {
  color: #222;
  line-height: 1.7;
  text-align: justify;
  white-space: pre-line;
}
.gallery {
  display: flex;
  gap: 16px;
  margin: 18px 32px 0 32px;
  flex-wrap: wrap;
}
.gallery-img {
  width: 260px;
  height: 170px;
  object-fit: cover;
  border-radius: 8px;
  background: #f8f8f8;
  box-shadow: 0 1px 6px #0001;
}
</style>