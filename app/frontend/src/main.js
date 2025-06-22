import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Toast, { POSITION } from 'vue-toastification';
import 'vue-toastification/dist/index.css';

const app = createApp(App);

app.use(router);
app.use(Toast, {
  position: POSITION.TOP_RIGHT,
  timeout: 2500,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
});

app.mount('#app');

// npm run serve