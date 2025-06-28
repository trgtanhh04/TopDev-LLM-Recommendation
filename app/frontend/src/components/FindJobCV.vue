<template>
  <LoadingPage v-if="loading" />
  <div
    v-else
    class="job-list-layout"
    style="display: flex; gap: 32px; padding: 32px 0 0 0; background: #f9f9f9;"
  >
    <!-- LEFT COLUMN -->
    <div class="main-panel">
      <!-- Upload CV Section -->
      <div class="upload-cv-section">
        <h2>Tải CV để được gợi ý công việc phù hợp</h2>
        <div class="upload-box">
          <input
            type="file"
            accept="application/pdf"
            @change="handleFileUpload"
          />
          <button :disabled="!cvFile" @click="submitCV">Gửi CV</button>
        </div>
        <!-- CV preview & filename -->
        <div v-if="cvFile" class="cv-preview-wrap">
          <a v-if="cvFile" :href="cvPreviewUrl" target="_blank" style="display:inline-block;margin-bottom:8px;color:#1976d2">{{ cvFile.name }}</a>
          <div class="cv-preview">
            <iframe
              v-if="cvPreviewUrl"
              :src="cvPreviewUrl"
              width="100%"
              height="420"
              style="border:1px solid #ddd; border-radius:8px;"
            ></iframe>
          </div>
        </div>
        <div v-if="uploadError" class="error">{{ uploadError }}</div>
      </div>

      <!-- Job List -->
      <h3 style="margin: 32px 0 12px;font-size:1.3rem;font-weight:700;color:#2e3a59">Việc làm tốt nhất</h3>
      <JobCard :jobs="jobs" :total-jobs="totalJobs" />

      <!-- Pagination -->
      <div class="paging-controls">
        <button :disabled="page === 1" @click="handlePageChange(page - 1)">
          ← Trước
        </button>
        <span>Trang {{ page }} / {{ totalPages }}</span>
        <button
          :disabled="page >= totalPages"
          @click="handlePageChange(page + 1)"
        >
          Sau →
        </button>
      </div>
    </div>

    <!-- RIGHT COLUMN -->
    <div class="recommendation-panel">
      <h3>Công việc phù hợp với bạn</h3>
      <ul v-if="recommendedJobs.length" class="job-suggest-list">
        <li
          v-for="job in recommendedJobs"
          :key="job.job_url"
          class="job-suggest-card"
          @click="goToJobDetail(job)"
          style="cursor: pointer;"
        >
          <div class="job-logo">
            <img
              v-if="getSmallImage(job.small_image)"
              :src="getSmallImage(job.small_image)"
              alt="Logo"
            />
          </div>
          <div class="job-content">
            <div class="job-header">
              <div class="job-title">{{ job.job_title }}</div>
              <div class="company-name">{{ job.company_name }}</div>
            </div>
            <div class="job-salary-row">
              <span class="salary">{{ job.salary }}</span>
              <template v-if="job.position_level && job.position_level.length">
                <span> • </span>
                <span>{{ job.position_level.join(", ") }}</span>
              </template>
              <template v-if="job.employment_type && job.employment_type.length">
                <span> • </span>
                <span>{{ job.employment_type.join(", ") }}</span>
              </template>
            </div>
            <div class="job-address-row">
              <span>{{ job.address }}</span>
              <template v-if="job.employment_type && job.employment_type.length">
                <span class="in-office">
                  ({{ job.employment_type.join(", ") }})
                </span>
              </template>
            </div>
            <div class="job-tags">
              <span
                v-for="tech in job.technologies_used"
                :key="tech"
                class="tag"
              >
                {{ tech }}
              </span>
            </div>
          </div>
        </li>
      </ul>
      <p v-else>Chưa có gợi ý nào.</p>
    </div>
  </div>
</template>

<script>
import JobCard from "./JobCard.vue";
import LoadingPage from "./LoadingPage.vue";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

export default {
  components: { JobCard, LoadingPage },
  data() {
    return {
      jobs: [],
      totalJobs: 0,
      page: 1,
      perPage: 15,
      loading: true,
      cvFile: null,
      cvPreviewUrl: "", // URL tạo từ File API để xem trước PDF
      uploadError: "",
      recommendedJobs: [],
      cvInfo: null,
    };
  },
  computed: {
    totalPages() {
      return Math.max(1, Math.ceil(this.totalJobs / this.perPage));
    },
  },
  created() {
    this.page = parseInt(this.$route.query.page) || 1;
    this.fetchJobs();
    // Lấy lại gợi ý nếu trước đó đã có (fix mất khi back lại)
    const jobs = localStorage.getItem("recommendedJobs");
    if (jobs) {
      this.recommendedJobs = JSON.parse(jobs);
    }
  },
  methods: {
    async fetchJobs() {
      NProgress.start();
      this.loading = true;
      try {
        const res = await fetch(
          `${process.env.VUE_APP_API_URL}/jobs?page=${this.page}&perPage=${this.perPage}`
        );
        const data = await res.json();
        this.jobs = data.jobs;
        this.totalJobs = data.total_jobs;
      } catch (e) {
        console.error("Error fetching jobs:", e);
      } finally {
        this.loading = false;
        NProgress.done();
      }
    },
    handlePageChange(newPage) {
      this.$router.push({
        path: this.$route.path,
        query: { ...this.$route.query, page: newPage },
      });
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.cvFile = file;
      this.uploadError = "";
      if (file && file.type === "application/pdf") {
        if (this.cvPreviewUrl) {
          URL.revokeObjectURL(this.cvPreviewUrl);
        }
        this.cvPreviewUrl = URL.createObjectURL(file);
      } else {
        this.cvPreviewUrl = "";
      }
    },
    getSmallImage(small_image) {
      if (!small_image) return '';
      if (Array.isArray(small_image)) {
        return small_image[0];
      }
      const match = small_image.match(/'(.*?)'/);
      return match ? match[1] : '';
    },
    async submitCV() {
      if (!this.cvFile) return;
      const formData = new FormData();
      formData.append("file", this.cvFile);

      try {
        NProgress.start();
        const res = await fetch(
          `${process.env.VUE_APP_API_URL}/process_cv`,
          {
            method: "POST",
            body: formData,
          }
        );

        if (!res.ok) throw new Error("Tải lên thất bại");
        const result = await res.json();
        this.recommendedJobs = result.matched_jobs;
        this.cvInfo = result.extracted_info; 
        // Lưu vào localStorage để khi back lại không mất gợi ý
        localStorage.setItem("recommendedJobs", JSON.stringify(this.recommendedJobs));
        localStorage.setItem("cvInfo", JSON.stringify(this.cvInfo));

      } catch (err) {
        this.uploadError = err.message;
      } finally {
        NProgress.done();
      }
    },
    goToJobDetail(job) {
      this.$router.push({
        name: "JobDetail",
        query: {
          job_title: job.job_title,
          company_name: job.company_name,
        },
      });
    },
  },
  beforeUnmount() {
    // Giải phóng URL khi component unmount để tránh memory leak
    if (this.cvPreviewUrl) {
      URL.revokeObjectURL(this.cvPreviewUrl);
    }
  },
};
</script>

<style scoped>
.job-list-layout {
  max-width: 1650px;
  margin: 0 auto;
}

.main-panel {
  flex: 1;
  max-width: 1050px;
  min-width: 0;
  background: transparent;
}

.upload-cv-section {
  background: white;
  padding: 32px 36px 28px 36px;
  border-radius: 16px;
  border: 1px solid #ddd;
  margin-bottom: 32px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.03);
}

.upload-cv-section h2 {
  margin-bottom: 18px;
  color: #1976d2;
  font-size: 2rem;
  font-weight: bold;
  letter-spacing: -.5px;
}

.upload-box {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.upload-box input[type="file"] {
  border: 1px dashed #bbb;
  padding: 8px 10px;
  border-radius: 7px;
  background: #f8f8f8;
  font-size: 1.08rem;
}

.upload-box button {
  background-color: #2196f3;
  color: white;
  padding: 8px 24px;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  transition: background 0.15s;
}

.upload-box button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.cv-filename {
  color: #1976d2;
  font-weight: 500;
  margin-left: 10px;
  font-size: 1.08rem;
  display:inline-block;
}

.cv-preview-wrap {
  margin-top: 10px;
  width: 100%;
  max-width: 850px;
}

.cv-preview {
  margin-top: 8px;
  width: 100%;
  max-width: 850px;
}

.error {
  color: red;
  margin-top: 10px;
}

.paging-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 28px;
  font-weight: bold;
}

.paging-controls button {
  padding: 8px 16px;
  background-color: #e0e0e0;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.08rem;
}

/* --- NEW STYLE FOR SUGGESTED JOBS LIKE IMAGE 2 --- */
.recommendation-panel {
  background: white;
  padding: 28px 22px;
  border-radius: 16px;
  border: 1px solid #ddd;
  max-width: 410px;
  width: 100%;
  box-shadow: 0 1px 8px rgba(0,0,0,0.03);
  margin-right: 24px;
  height: fit-content;
}

.recommendation-panel h3 {
  font-size: 1.4rem;
  color: #2e3a59;
  font-weight: 700;
  margin-bottom: 18px;
}

.job-suggest-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.job-suggest-card {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  background: #eaf5ff;
  border-radius: 12px;
  margin-bottom: 22px;
  padding: 18px 18px 14px 18px;
  box-shadow: 0 1px 4px #0001;
  cursor: pointer;
  transition: box-shadow 0.18s, background 0.15s;
}
.job-suggest-card:hover {
  box-shadow: 0 4px 16px #1976d24c;
  background: #def3ff;
}

.job-logo img {
  width: 58px;
  height: 58px;
  object-fit: contain;
  border-radius: 10px;
  background: #fff;
  border: 1px solid #cce5ff;
}

.job-content {
  flex: 1;
  min-width: 0;
}

.job-header {
  margin-bottom: 4px;
}

.job-title {
  font-weight: 700;
  font-size: 1.09rem;
  color: #222;
  margin-bottom: 2px;
}

.company-name {
  font-size: 1rem;
  font-weight: 500;
  color: #1976d2;
  text-transform: uppercase;
  margin-bottom: 2px;
}

.job-salary-row {
  color: #d32f2f;
  font-size: 1rem;
  margin-bottom: 2px;
  font-weight: 500;
}

.salary {
  color: #d32f2f;
}

.job-address-row {
  font-size: 1rem;
  color: #222;
  margin-bottom: 4px;
}

.in-office {
  color: #888;
  margin-left: 4px;
}

.job-tags {
  margin-top: 6px;
}

.tag {
  display: inline-block;
  background: #fff;
  color: #1976d2;
  font-weight: 500;
  border-radius: 6px;
  padding: 3px 12px;
  font-size: 0.98rem;
  margin-right: 7px;
  margin-bottom: 2px;
  border: 1px solid #cce5ff;
}

@media (max-width: 1200px) {
  .main-panel, .cv-preview, .cv-preview-wrap {
    max-width: 100%;
  }
  .job-list-layout {
    flex-direction: column;
    padding: 18px 6px;
  }
  .recommendation-panel {
    max-width: 100%;
    margin-right: 0;
    margin-top: 24px;
  }
}
</style>