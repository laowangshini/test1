import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    isGuest: false
  },
  getters: {
    isAuthenticated: state => !!state.token || state.isGuest,
    isGuest: state => state.isGuest,
    currentUser: state => state.user,
    canAccess: state => (feature) => {
      if (state.isGuest) {
        // 游客只能访问资料广场
        return feature === 'square';
      }
      return !!state.token;
    }
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
    clearAuth(state) {
      state.token = '';
      state.user = null;
      state.isGuest = false;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    },
    setGuestMode(state, isGuest) {
      state.isGuest = isGuest;
      if (isGuest) {
        state.user = {
          username: '游客',
          display_name: '游客',
          user_type: 'guest'
        };
      }
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/auth/login/', credentials);
        if (!response.data || !response.data.user) {
          throw new Error('登录响应格式错误');
        }
        
        const user = response.data.user;
        const token = response.data.token || 'dummy-token';
        
        commit('setToken', token);
        commit('setUser', user);
        return response;
      } catch (error) {
        commit('clearAuth');
        throw error;
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('/api/auth/logout/');
      } catch (error) {
        console.error('登出错误:', error);
      } finally {
        commit('clearAuth');
      }
    },
    async register({ commit }, userData) {
      try {
        const response = await axios.post('/api/auth/register/', userData);
        const { token, user } = response.data;
        commit('setToken', token);
        commit('setUser', user);
        return response;
      } catch (error) {
        commit('clearAuth');
        throw error;
      }
    },
    async fetchUserInfo({ commit }) {
      try {
        const response = await axios.get('/api/auth/user-info/');
        commit('setUser', response.data);
        return response;
      } catch (error) {
        commit('clearAuth');
        throw error;
      }
    }
  }
})
