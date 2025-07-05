<template>
  <div class="loading-page">
    <div class="spinner"></div>
    <div class="loading-message">
      Đang tải dữ liệu, vui lòng chờ...
      <br />
      <span style="color:#1976d2;">
        Nếu bạn phải chờ quá lâu, có thể backend đang khởi động.<br />
      </span>
    </div>
  </div>
</template>

<style scoped>
.loading-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
}
.spinner {
  border: 6px solid #e3f2fd;
  border-top: 6px solid #1976d2;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}
.loading-message {
  font-size: 1.08rem;
  text-align: center;
  margin-top: 8px;
  max-width: 1300px;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
</style>