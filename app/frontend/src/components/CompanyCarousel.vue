<template>
  <div>
    <h2 class="section-title">Công ty đề xuất</h2>
    <div id="companyCarousel" class="carousel slide" data-ride="carousel" data-interval="5000">
      <div class="carousel-inner">
        <div
          v-for="(group, idx) in companyGroups"
          :key="idx"
          :class="['carousel-item', { active: idx === 0 }]"
        >
          <div class="row">
            <div
              v-for="company in group"
              :key="company.name"
              class="col-md-3"
            >
              <router-link
                class="company-card"
                :to="{
                  path: '/company-detail',
                  query: { company_name: company.name }
                }"
                style="text-decoration: none; color: inherit; cursor: pointer;"
              >
                <div class="company-image">
                  <img :src="getBigImage(company.big_image)" alt="Banner" />
                </div>
                <div class="company-info">
                  <div class="company-logo-row">
                    <img :src="getSmallImage(company.small_image)" alt="Logo" class="company-logo" />
                    <div>
                      <div class="company-name clamp-2">{{ company.name }}</div>
                    </div>
                  </div>
                  <div class="company-tagline-address">
                    <div class="company-tagline">{{ company.tag_line }}</div>
                    <div class="company-address">
                      {{ parseStringToArray(company.office_address).join(', ') }}
                    </div>
                  </div>
                  <div class="company-industry-more">
                    <span class="company-industry">
                      {{ parseStringToArray(company.industry).join(', ') }}
                    </span>
                    <span class="more-link">More...</span>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <a class="carousel-control-prev custom-arrow" href="#companyCarousel" role="button" data-slide="prev">
        <span class="carousel-arrow-icon" aria-hidden="true">&#8592;</span>
      </a>
      <a class="carousel-control-next custom-arrow" href="#companyCarousel" role="button" data-slide="next">
        <span class="carousel-arrow-icon" aria-hidden="true">&#8594;</span>
      </a>
    </div>
  </div>
</template>

<script>
import { parseStringToArray } from '../utils/parseStringToArray';

export default {
  name: 'CompanyCarousel',
  props: {
    companies: {
      type: Array,
      required: true
    }
  },
  computed: {
    companyGroups() {
      const groups = [];
      for (let i = 0; i < this.companies.length; i += 4) {
        groups.push(this.companies.slice(i, i + 4));
      }
      return groups;
    },
  },
  methods: {
    parseStringToArray,
    getSmallImage(img) {
      const arr = this.parseStringToArray(img);
      return arr.length ? arr[0] : '';
    },
    getBigImage(img) {
      const arr = this.parseStringToArray(img);
      return arr.length ? arr[0] : '';
    }
  },
  mounted() {
    this.$nextTick(() => {
      // Set interval to 5 seconds (5000ms)
      window.$('#companyCarousel').carousel({ interval: 5000, ride: 'carousel' });
    });
  },
  watch: {
    companies() {
      this.$nextTick(() => {
        window.$('#companyCarousel').carousel({ interval: 5000, ride: 'carousel' });
      });
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
.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 28px;
  color: #222;
  text-align: left;
}
.company-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px #0001;
  margin: 12px 8px 24px 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.18s;
  min-height: 400px;
  height: 400px;
}
.company-card:hover {
  box-shadow: 0 4px 24px #1976d233;
}
.company-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  background: #f8f8f8;
}
.company-info {
  padding: 18px 16px 36px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  position: relative;
  min-height: 210px;
}
.company-logo-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.company-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 8px;
  background: #f8f8f8;
  border: 1px solid #eee;
}
.company-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #1976d2;
  line-height: 1.2;
  margin-bottom: 0;
  max-width: 180px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
}
.clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
}
.company-tagline-address {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 4px;
  font-size: 1rem;
}
.company-tagline {
  color: #222;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.company-address {
  color: #444;
  font-size: 1rem;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.company-industry-more {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 28px;
  margin-top: auto;
}
.company-industry {
  color: #888;
  font-size: 0.98rem;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
}
.more-link {
  color: #ff5a36;
  font-weight: 500;
  text-decoration: underline;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  margin-left: 8px;
}
.more-link:hover {
  color: #d32f2f;
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