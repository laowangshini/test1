<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo-container">
        <img src="@/assets/logo.png" alt="Logo" class="logo">
      </div>
      <h2>欢迎来到人类学家的资料库</h2>
      <p class="subtitle">探索人文 记录文化</p>
      
      <el-form
        ref="loginForm"
        :model="form"
        :rules="rules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <div class="button-group">
          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
          <el-button
            class="register-btn"
            @click="$router.push('/register')"
          >
            注册
          </el-button>
        </div>
      </el-form>
      
      <div class="guest-link">
        只是想看看？
        <el-link type="info" @click="handleGuestLogin">
          以游客身份访问
        </el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const store = useStore()
const loginForm = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9]+$/, message: '用户名只能包含数字和英文字母', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度必须在8-20位之间', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    // 验证表单
    const valid = await loginForm.value.validate();
    if (!valid) {
      return;
    }

    loading.value = true;
    
    // 使用正确的API路径
    const response = await axios.post('/api/auth/login/', form);
    
    // 保存token和用户信息
    store.commit('SET_TOKEN', response.data.token);
    store.commit('SET_USER', response.data.user);
    
    ElMessage.success('登录成功');
    
    // 添加延时确保状态更新
    await nextTick();
    // 使用 replace 而不是 push，防止用户点击返回回到登录页
    await router.replace('/dashboard');
  } catch (error) {
    console.error('登录失败:', error);
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error);
    } else {
      ElMessage.error('登录失败，请稍后重试');
    }
  } finally {
    loading.value = false;
  }
};

const handleGuestLogin = async () => {
  try {
    // 设置游客状态
    await store.commit('setGuestMode', true);
    ElMessage.success('正在以游客身份访问');
    await router.push('/dashboard');
  } catch (error) {
    console.error('游客访问失败:', error);
    ElMessage.error('访问失败，请稍后重试');
  }
};
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url('@/assets/background.jpg') no-repeat center center;
  background-size: cover;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
  }
  
  .login-box {
    position: relative;
    width: 400px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    
    .logo-container {
      text-align: center;
      margin-bottom: 24px;
      
      .logo {
        height: 150px;
        width: auto;
        object-fit: contain;
      }
    }
    
    h2 {
      margin: 0;
      text-align: center;
      color: #2c3e50;
      font-size: 24px;
      font-weight: 500;
    }
    
    .subtitle {
      margin: 8px 0 32px;
      text-align: center;
      color: #606266;
      font-size: 14px;
    }
    
    .login-form {
      .button-group {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
        
        .submit-btn, .register-btn {
          flex: 1;
          height: 48px;
          padding: 12px;
          font-size: 16px;
        }

        .register-btn {
          background-color: #409eff;
          border-color: #409eff;
          color: white;
          
          &:hover {
            background-color: #66b1ff;
            border-color: #66b1ff;
          }
        }
      }
    }
    
    .guest-link {
      margin-top: 24px;
      text-align: center;
      font-size: 14px;
      color: #606266;
      
      .el-link {
        font-size: 14px;
        margin-left: 4px;
      }
    }
  }
}

:deep(.el-input__wrapper) {
  padding: 0 12px;
  height: 44px;
  box-shadow: 0 0 0 1px #dcdfe6 inset;
  
  &:hover {
    box-shadow: 0 0 0 1px #c0c4cc inset;
  }
  
  &.is-focus {
    box-shadow: 0 0 0 1px #409eff inset;
  }
  
  .el-input__inner {
    font-size: 14px;
  }
}
</style> 