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
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
};
</script>

<style scoped>
.nav-bar {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 16px 32px;
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
</style>