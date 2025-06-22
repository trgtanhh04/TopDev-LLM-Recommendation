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
        <li><router-link to="/process_cv">Tìm việc làm</router-link></li>
      </ul>
      <div class="nav-actions">
        <template v-if="userName">
          <span>Xin chào, {{ userName }}</span>
          <button class="logout-btn" @click="handleLogout">Đăng xuất</button>
        </template>
        <button v-else class="google-login-btn" @click="handleGoogleLogin">
          <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" class="google-icon" />
          Đăng nhập
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { jwtDecode } from "jwt-decode";
import { useToast } from "vue-toastification";

export default {
  name: "NavBar",
  data() {
    return {
      userName: null,
      toast: null,
    };
  },
  created() {
    // Get the toast instance for use in methods
    this.toast = useToast();
    this.checkLogin();
  },
  methods: {
    handleGoogleLogin() {
      const backendUrl = process.env.VUE_APP_API_URL;
      // Use full URL, not just path
      const next = encodeURIComponent(window.location.origin + window.location.pathname + window.location.search);
      window.location.href = `${backendUrl}/auth/google/login?next=${next}`;
    },
    handleLogout() {
      localStorage.removeItem("jwt_token");
      this.userName = null;
      this.toast.success("Đăng xuất thành công!");
      this.$router.push("/");
    },
    checkLogin() {
      let token = localStorage.getItem("jwt_token");
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.has("token")) {
        token = urlParams.get("token");
        localStorage.setItem("jwt_token", token);
        urlParams.delete("token");
        const newUrl =
          window.location.pathname +
          (urlParams.toString() ? "?" + urlParams.toString() : "");
        window.history.replaceState({}, document.title, newUrl);
        this.toast.success("Đăng nhập thành công!");
      }
      if (token) {
        try {
          const payload = jwtDecode(token);
          this.userName = payload.name;
        } catch (e) {
          this.userName = null;
        }
      } else {
        this.userName = null;
      }
    },
  },
  watch: {
    $route() {
      this.checkLogin();
    },
  },
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

.logout-btn {
  margin-left: 12px;
  background: #fff;
  border: 1px solid #e53935;
  color: #e53935;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #ffebee;
}
</style>