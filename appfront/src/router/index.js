import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  // 添加一个重定向
  {
    path: '/',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.token || store.state.isGuest
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要认证但未登录，重定向到登录页
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // 已登录但访问登录页，重定向到首页
    next('/dashboard')
  } else {
    next()
  }
})

export default router
