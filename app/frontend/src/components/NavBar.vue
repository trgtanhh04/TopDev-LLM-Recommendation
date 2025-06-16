<template>
  <nav class="nav-bar">
    <div class="nav-container">
      <div class="nav-logo">
        <img src="@/assets/logo.png" alt="Logo" />
      </div>
      <ul class="nav-links">
        <li><router-link to="/">Trang chủ</router-link></li>
        <li><router-link to="/viec-lam-it">Việc làm</router-link></li>
        <li><router-link to="/cong-ty">Công ty</router-link></li>
        <li><router-link to="/cong-cu">Công cụ</router-link></li>
        <li><router-link to="/blog-it">Blog IT</router-link></li>
      </ul>
      <div class="nav-actions">
        <button class="google-login-btn" @click="handleGoogleLogin">
          <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" class="google-icon" />
          Đăng nhập
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  methods: {
    handleGoogleLogin() {
      // Use the backend URL from .env
      const backendUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000';
      console.log("Redirecting to:", `${backendUrl}/auth/google/login`);
      window.location.href = `${backendUrl}/auth/google/login`;
    }
  }
};
</script>

<style scoped>
.nav-bar {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 16px 0 16px 0;
  background: #f4faff;
  box-shadow: 0 1px 6px #0001;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.nav-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.nav-logo img {
  height: 36px;
}

.nav-links {
  display: flex;
  gap: 32px;
  list-style: none;
  margin: 0 auto;
  padding: 0;
  position: absolute;
  left: 0;
  right: 0;
  justify-content: center;
}

.nav-links li {
  font-size: 16px;
}

.nav-links a {
  color: #1976d2;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a.router-link-exact-active {
  color: #0d47a1;
  border-bottom: 2px solid #1976d2;
}

.nav-actions {
  display: flex;
  align-items: center;
}

.google-login-btn {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #1976d2;
  color: #1976d2;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  gap: 8px;
}

.google-login-btn:hover {
  background: #e3f2fd;
}

.google-icon {
  width: 20px;
  height: 20px;
}
</style>