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

// 配置 axios 默认值
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.timeout = 10000
axios.defaults.withCredentials = true  // 允许跨域携带 cookie

// 请求拦截器
axios.interceptors.request.use(
  config => {
    console.log('发送请求:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    });
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
axios.interceptors.response.use(
  response => {
    console.log('收到响应:', {
      status: response.status,
      headers: response.headers,
      data: response.data
    });
    
    // 如果响应中包含用户信息，更新到 store
    if (response.data && response.data.user) {
      store.commit('setUser', response.data.user);
    }
    
    return response;
  },
  error => {
    console.error('响应错误:', {
      message: error.message,
      response: error.response,
      request: error.request
    });
    
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除 token 并跳转到登录页面
          store.commit('clearAuth');
          router.push('/login');
          ElMessage.error('登录已过期，请重新登录');
          break;
        case 403:
          // 权限不足
          ElMessage.error('权限不足');
          break;
        case 404:
          // 请求的资源不存在
          ElMessage.error('请求的资源不存在');
          break;
        case 500:
          // 服务器错误
          ElMessage.error('服务器错误，请稍后重试');
          break;
        default:
          ElMessage.error(error.response.data?.message || '发生错误，请稍后重试');
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      ElMessage.error('无法连接到服务器，请检查网络连接');
    } else {
      // 请求配置出错
      ElMessage.error('请求配置错误');
    }
    
    return Promise.reject(error);
  }
);

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
