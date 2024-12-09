import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 确保baseURL配置正确
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.timeout = 10000
axios.defaults.withCredentials = true

// 添加请求拦截器用于调试
axios.interceptors.request.use(
  config => {
    console.log('发送请求:', {
      url: config.url,
      method: config.method,
      data: config.data,
      headers: config.headers
    })
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 添加响应拦截器用于调试
axios.interceptors.response.use(
  response => {
    console.log('收到响应:', {
      status: response.status,
      data: response.data,
      headers: response.headers
    })
    return response
  },
  error => {
    console.error('响应错误:', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers
    })
    return Promise.reject(error)
  }
)

const app = createApp(App);

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 全局属性
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$echarts = echarts;

// 初始化应用
const init = async () => {
  try {
    // 如果本地存储有用户信息，尝试恢复会话
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      await store.dispatch('fetchUserInfo');
    }
  } catch (error) {
    console.error('初始化失败:', error);
    // 如果恢复会话失败，清除本地存储
    store.commit('clearAuth');
  } finally {
    // 无论成功失败，都要挂载应用
    app.use(store)
       .use(router)
       .use(ElementPlus)
       .mount("#app");
  }
};

init();
