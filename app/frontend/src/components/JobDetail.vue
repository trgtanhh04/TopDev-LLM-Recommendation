<template>
  <div v-if="loading">
    <LoadingPage />
  </div>
  <div v-else-if="jobDetail" class="job-detail-card">
    <div class="header-row">
      <img class="company-logo" :src="companyLogo" alt="logo" v-if="companyLogo" />
      <div class="header-info">
        <div class="company-name">{{ jobDetail.company_name }}</div>
        <div class="job-title">{{ jobDetail.job_title }}</div>
        <div class="location-row">
          <span class="info-icon">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none"><path d="M10 18s6-5.686 6-10A6 6 0 1 0 4 8c0 4.314 6 10 6 10z" fill="#1976d2"/><circle cx="10" cy="8" r="2.5" fill="#fff"/></svg>
          </span>
          <span>{{ parseStringToArray(jobDetail.address)[0] }}</span>
        </div>
      </div>
      <div class="header-actions">
        <button class="apply-btn">Ứng tuyển ngay</button>
        <button class="cv-btn" @click="compareWithCV">So sánh với CV</button>
      </div>
    </div>
        <!--Advice Loading -->
    <div v-if="adviceLoading" class="advice-box">
      <p>🔍 Đang phân tích CV...</p>
    </div>

    <!-- Advice Result -->
    <div v-if="advice" class="advice-box">
      <h4>🎯 Kết quả so sánh CV với công việc</h4>
      <p><strong>Điểm phù hợp:</strong> {{ advice.match_score }} / 100</p>
      <p><strong>Kỹ năng còn thiếu:</strong> {{ advice.missing_skills?.join(', ') || 'Không có' }}</p>
      <p><strong>Lời khuyên:</strong> {{ advice.summary }}</p>
      <div v-if="advice.recommendations?.length">
        <h5>📚 Khóa học gợi ý:</h5>
        <ul>
          <li v-for="(rec, index) in advice.recommendations" :key="index">
            <strong>{{ rec.skill }}</strong>:
            <a :href="rec.link" target="_blank" rel="noopener">{{ rec.course }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="main-row">
      <div class="salary">
        <span class="main-svg">
          <svg width="22" height="22" fill="none" viewBox="0 0 22 22"><rect x="2" y="6" width="18" height="10" rx="3" fill="#ffe0e0"/><rect x="2" y="6" width="18" height="3" fill="#ffbdbd"/><circle cx="11" cy="11" r="2.5" fill="#d32f2f"/><rect x="6" y="9" width="2" height="4" rx="1" fill="#fff"/><rect x="14" y="9" width="2" height="4" rx="1" fill="#fff"/></svg>
        </span>
        <span class="salary-text">{{ jobDetail.salary }}</span>
      </div>
      <div class="meta">
        <span class="main-svg">
          <svg width="22" height="22" fill="none" viewBox="0 0 22 22"><circle cx="11" cy="11" r="9" fill="#e3f2fd"/><circle cx="11" cy="11" r="8" stroke="#bfc8e6" stroke-width="1.5"/><rect x="10.25" y="6.5" width="1.5" height="5" rx="0.75" fill="#bfc8e6"/><rect x="11" y="11" width="4" height="1.5" rx="0.75" transform="rotate(45 11 11)" fill="#bfc8e6"/></svg>
        </span>
        <span>
          {{ parseStringToArray(jobDetail.date_posted)[0] }}
        </span>
      </div>
      <div class="tech-tags">
        <span class="main-svg">
          <svg width="22" height="22" fill="none" viewBox="0 0 22 22"><rect x="4" y="7" width="14" height="8" rx="2" fill="#e3f2fd"/><rect x="7" y="10" width="8" height="2" rx="1" fill="#bfc8e6"/><rect x="9" y="12" width="4" height="2" rx="1" fill="#bfc8e6"/><rect x="9" y="8" width="4" height="2" rx="1" fill="#bfc8e6"/></svg>
        </span>
        <span
          v-for="tech in parseStringToArray(jobDetail.technologies_used)"
          :key="tech"
          class="tech-tag"
        >{{ tech }}</span>
      </div>
    </div>
    <div class="info-row">
      <div class="info-block">
        <div class="info-icon">📅</div>
        <div>
          <div class="info-label">Năm kinh nghiệm tối thiểu</div>
          <div class="info-value">{{ parseStringToArray(jobDetail.experience_years)[0] }}</div>
        </div>
      </div>
      <div class="info-block">
        <div class="info-icon">🎓</div>
        <div>
          <div class="info-label">Cấp bậc</div>
          <div class="info-value">{{ parseStringToArray(jobDetail.position_level).join(', ') }}</div>
        </div>
      </div>
      <div class="info-block">
        <div class="info-icon">🏢</div>
        <div>
          <div class="info-label">Loại hình</div>
          <div class="info-value">{{ parseStringToArray(jobDetail.employment_type).join(', ') }}</div>
        </div>
      </div>
      <div class="info-block">
        <div class="info-icon">📄</div>
        <div>
          <div class="info-label">Loại hợp đồng</div>
          <div class="info-value">{{ parseStringToArray(jobDetail.contract_type).join(', ') }}</div>
        </div>
      </div>
    </div>
    <div class="desc">
      <template v-for="(section, idx) in parsedSections" :key="idx">
        <div class="desc-section" :class="section.key">
          <div class="desc-section-header">
            <span class="desc-section-icon" v-if="section.icon" v-html="section.icon"></span>
            {{ section.title }}
          </div>
          <div class="desc-section-list">
            <template v-for="(item, i) in section.items" :key="i">
              <div
                v-if="isNumberedLine(item)"
                class="desc-no-bullet"
              >{{ item }}</div>
              <div
                v-else
                class="desc-list-item"
              >{{ item }}</div>
            </template>
          </div>
        </div>
      </template>
    </div>
    <div class="company-section">
      <div class="company-header">
        <div class="company-title">
          Thông tin về
          <router-link
            :to="{
              name: 'CompanyDetail',
              query: { company_name: jobDetail.company_name }
            }"
            style="color:#1976d2;text-decoration:underline;cursor:pointer"
          >
            {{ jobDetail.company_name }}
          </router-link>
        </div>
        <a
          v-if="jobDetail.company_url"
          :href="parseStringToArray(jobDetail.company_url)[0]"
          target="_blank"
          rel="noopener"
          class="company-link"
        >{{ parseStringToArray(jobDetail.company_url)[0] }}</a>
      </div>
      <div class="company-meta-row">
        <div class="info-company-block">
          <div class="info-icon">🏢</div>
          <div>
            <div class="info-label">Ngành nghề</div>
            <div class="info-value">{{ parseStringToArray(jobDetail.industry)[0] }}</div>
          </div>
        </div>
        <div class="info-company-block">
          <div class="info-icon">👥</div>
          <div>
            <div class="info-label">Quy mô công ty</div>
            <div class="info-value">{{ parseStringToArray(jobDetail.company_size)[0] }}</div>
          </div>
        </div>
        <div class="info-company-block">
          <div class="info-icon">🏳️</div>
          <div>
            <div class="info-label">Quốc tịch công ty</div>
            <div class="info-value">{{ parseStringToArray(jobDetail.company_nationality)[0] }}</div>
          </div>
        </div>
      </div>
      <div class="company-profile-block">
        <h4>Giới thiệu công ty</h4>
        <div class="company-profile-paragraph">
          {{ parseCompanyProfile(jobDetail.company_profile) }}
        </div>
      </div>
      <div
        v-if="parseStringToArray(jobDetail.image_galleries).filter(img => img && img.trim()).length"
        class="company-gallery"
      >
        <div
          v-for="(img, idx) in parseStringToArray(jobDetail.image_galleries).filter(img => img && img.trim())"
          :key="idx"
          class="company-gallery-img"
        >
          <img :src="img" alt="Ảnh công ty" />
        </div>
      </div>
      <div class="see-more-link-wrapper">
        <router-link
          v-if="jobDetail && jobDetail.company_name"
          :to="{
            name: 'CompanyDetail',
            query: { company_name: jobDetail.company_name }
          }"
          class="see-more-link"
        >
          Xem thêm...
        </router-link>
      </div>
    </div>
  </div>
  <div v-else>
    Không tìm thấy thông tin công việc.
  </div>
</template>

<script>
import LoadingPage from './LoadingPage.vue';
import { parseStringToArray } from '../utils/parseStringToArray';
import { parseJobDescriptionToSections } from '../utils/parseJobDescription';
import { parseCompanyProfile } from '../utils/parseCompanyProfile';

export default {
  components: { LoadingPage },
  data() {
    return {
      jobDetail: null,
      loading: true,
      advice: null,
      adviceLoading: false,
      adviceError: null,
    };
  },
  computed: {
    parsedSections() {
      if (!this.jobDetail) return [];
      // Remove the "Quy trình phỏng vấn" section if present
      return parseJobDescriptionToSections(this.jobDetail.job_description)
        .filter(section => section.key !== 'interview');
    },
    companyLogo() {
      if (!this.jobDetail) return '';
      const arr = this.parseStringToArray(this.jobDetail.small_image);
      return arr.length ? arr[0] : '';
    }
  },
  created() {
    this.loadJobDetail(); // Gọi method bạn tự định nghĩa
  },
  methods: {
    parseStringToArray,
    parseCompanyProfile,
    isNumberedLine(line) {
      return /^\d+\./.test(line);
    },
    async compareWithCV() {
      console.log('🔥 Button clicked!');
      alert('Đã nhấn nút So sánh với CV');
      this.adviceLoading = true;
      this.advice = null;
      this.adviceError = null;

      try {
        const cvInfoStr = localStorage.getItem("cvInfo");
        if (!cvInfoStr) {
          this.adviceError = "Không tìm thấy thông tin CV trong localStorage.";
          return;
        }

        const cvInfo = JSON.parse(cvInfoStr);
        const jobInfo = this.jobDetail;

        const res = await fetch(`${process.env.VUE_APP_API_URL}/give_advice`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ cv_info: cvInfo, job_info: jobInfo })
        });

        if (!res.ok) throw new Error("Lỗi từ server");

        const result = await res.json();
        this.advice = result;
      } catch (err) {
        this.adviceError = err.message;
      } finally {
        this.adviceLoading = false;
      }
    },
    async loadJobDetail() {
      const { job_title, company_name } = this.$route.query;
      if (!job_title || !company_name) {
        this.loading = false;
        return;
      }
      try {
        const url = `${process.env.VUE_APP_API_URL}/job-detail?job_title=${encodeURIComponent(job_title)}&company_name=${encodeURIComponent(company_name)}`;
        const res = await fetch(url);
        const data = await res.json();
        this.jobDetail = data.job_detail;
      } catch (e) {
        this.jobDetail = null;
      } finally {
        this.loading = false;
      }
    },
  }
};
</script>
<style scoped>

.job-detail-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #0001;
  padding: 28px 32px 18px 32px;
  max-width: 1120px;
  margin: 32px auto;
  font-family: Arial, sans-serif;
}
.header-row {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  border-bottom: 1px solid #eee;
  padding-bottom: 18px;
}
.company-logo {
  width: 70px;
  height: 70px;
  object-fit: contain;
  border-radius: 10px;
  background: #f8f8f8;
  margin-right: 8px;
}
.header-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.company-name {
  color: #ff5a36;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 2px;
  text-transform: uppercase;
}
.job-title {
  font-size: 22px;
  font-weight: bold;
  color: #222;
  margin-bottom: 4px;
}
.location-row {
  display: flex;
  align-items: center;
  color: #888;
  font-size: 16px;
  margin-top: 2px;
  gap: 6px;
}
.header-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}
.apply-btn {
  background: #ff5a36;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 22px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 4px;
}
.cv-btn {
  background: #fff;
  color: #ff5a36;
  border: 1px solid #ff5a36;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 4px;
}
.icon-btn {
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  margin-bottom: 2px;
}
.main-row {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
}
.salary {
  display: flex;
  align-items: center;
  gap: 6px;
}
.salary-text {
  color: #d32f2f;
  font-size: 18px;
  font-weight: bold;
}
.meta {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #444;
  font-size: 16px;
}
.tech-tags {
  display: flex;
  align-items: center;
  gap: 6px;
}
.tech-tag {
  background: #e3f2fd;
  color: #1976d2;
  font-size: 14px;
  padding: 2px 12px;
  border-radius: 6px;
  font-weight: 500;
}
.main-svg {
  display: flex;
  align-items: center;
  margin-right: 4px;
}
.dot {
  font-size: 18px;
  margin: 0 4px;
}
.info-row {
  display: flex;
  gap: 110px;
  margin-top: 28px;
  border-top: 1px solid #eee;
  padding-top: 18px;
}
.info-block {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  min-width: 180px;
}
.info-company-block {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  min-width: 300px;
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
.desc {
  margin-top: 32px;
  margin-bottom: 24px;
  white-space: pre-line;
}
.desc-section {
  margin-bottom: 28px;
  padding: 18px 20px;
  border-radius: 10px;
  background: #f8fafd;
  box-shadow: 0 1px 6px #0001;
}
.desc-section-header {
  font-size: 18px;
  font-weight: bold;
  color: #d32f2f;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.desc-section-icon {
  font-size: 20px;
}
.desc-section.responsibility { background: #fff5f5; }
.desc-section.skill { background: #f7fbff; }
.desc-section.benefit { background: #fffef3; }
.desc-section-list {
  padding-left: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.desc-list-item {
  margin-left: 18px;
  position: relative;
  padding-left: 24px;
}
.desc-list-item::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #888;
  font-weight: bold;
}
.desc-no-bullet {
  margin-left: 0;
  font-weight: bold;
  color: #1976d2;
  padding-left: 0;
  margin-top: 10px;
  margin-bottom: 10px;
}
.company-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 6px #0001;
  padding: 24px 28px 18px 28px;
  margin-top: 32px;
}
.company-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.company-title {
  font-size: 20px;
  font-weight: bold;
  color: #222;
}
.company-link {
  color: #1976d2;
  font-size: 15px;
  text-decoration: underline;
  margin-left: 16px;
  word-break: break-all;
}
.company-meta-row {
  display: flex;
  gap: 110px;
  margin-bottom: 18px;
  margin-top: 8px;
  padding: 10px 0 24px 0;
  justify-content: flex-start;
}
.company-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 200px;
  gap: 0;
}
.company-meta-icon {
  font-size: 22px;
  margin-bottom: 2px;
}
.company-meta-label {
  font-weight: bold;
  color: #222;
  font-size: 17px;
  margin-bottom: 2px;
}
.company-meta-value {
  font-size: 17px;
  color: #444;
  margin-top: 2px;
  font-weight: 500;
}
.company-profile-block {
  margin-bottom: 18px;
}
.company-profile-block h4 {
  margin-bottom: 8px;
  color: #d32f2f;
}
.company-gallery {
  display: flex;
  gap: 16px;
  margin-top: 10px;
  flex-wrap: wrap;
}
.company-gallery-img img {
  width: 260px;
  height: 170px;
  object-fit: cover;
  border-radius: 8px;
  background: #f8f8f8;
  box-shadow: 0 1px 6px #0001;
}
.company-profile-paragraph {
  margin-bottom: 8px;
  line-height: 1.7;
  color: #222;
  white-space: pre-line;
  text-align: justify;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Advice */
.advice-box {
  background: #f1f8e9;
  border-left: 6px solid #8bc34a;
  padding: 20px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 10px #0001;
  margin-top: 32px;
  font-family: Arial, sans-serif;
  color: #2e3a59;
  max-width: 100%;
}

.advice-box h4 {
  margin-bottom: 12px;
  font-size: 18px;
  font-weight: bold;
  color: #558b2f;
}

.advice-box h5 {
  margin-top: 16px;
  margin-bottom: 8px;
  font-size: 16px;
  color: #33691e;
}

.advice-box ul {
  padding-left: 20px;
  margin: 0;
}

.advice-box li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.advice-error {
  background: #ffebee;
  border-left: 6px solid #d32f2f;
  color: #b71c1c;
  padding: 16px 20px;
  margin-top: 24px;
  border-radius: 10px;
  font-weight: 500;
  max-width: 100%;
}

.see-more-link-wrapper {
  width: 100%;
  text-align: right;
  margin-top: 18px;
}

.see-more-link {
  display: inline-block;
  color: #1976d2;
  font-weight: 500;
  font-size: 16px;
  text-decoration: underline;
  cursor: pointer;
  transition: color 0.2s;
}

.see-more-link:hover {
  color: #0d47a1;
}

</style>

