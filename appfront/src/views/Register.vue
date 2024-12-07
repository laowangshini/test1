<template>
  <div class="register-container">
    <div class="register-box">
      <h2>注册账号</h2>
      <p class="subtitle">加入人类学家的资料库</p>
      
      <el-form
        ref="registerForm"
        :model="form"
        :rules="rules"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="ID（4-20位字母或数字）"
            :prefix-icon="User"
          >
            <template #append>
              <el-tooltip
                content="ID只能包含字母和数字，长度4-20位"
                placement="top"
              >
                <el-icon><info-filled /></el-icon>
              </el-tooltip>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="display_name">
          <el-input
            v-model="form.display_name"
            placeholder="用户名（显示名称）"
            :prefix-icon="User"
          >
            <template #append>
              <el-tooltip
                content="用户名将显示在您的个人资料和发布的内容中"
                placement="top"
              >
                <el-icon><info-filled /></el-icon>
              </el-tooltip>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码（8-20位，包含字母和数字）"
            :prefix-icon="Lock"
            show-password
          >
            <template #append>
              <el-tooltip
                content="密码长度8-20位，必须包含字母和数字"
                placement="top"
              >
                <el-icon><info-filled /></el-icon>
              </el-tooltip>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="确认密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-link">
        已有账号？
        <el-link type="primary" @click="$router.push('/login')">
          立即登录
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
import { User, Lock, InfoFilled } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const store = useStore()
const registerForm = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  display_name: '',
  password: '',
  confirmPassword: ''
})

const validateUsername = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入ID'))
  } else if (value.length < 4 || value.length > 20) {
    callback(new Error('ID长度必须在4-20位之间'))
  } else if (!/^[a-zA-Z0-9]+$/.test(value)) {
    callback(new Error('ID只能包含字母和数字'))
  } else {
    callback()
  }
}

const validateDisplayName = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入用户名'))
  } else if (value.length > 50) {
    callback(new Error('用户名长度不能超过50个字符'))
  } else {
    callback()
  }
}

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (value.length < 8 || value.length > 20) {
    callback(new Error('密码长度必须在8-20位之间'))
  } else if (!(/[A-Za-z]/.test(value) && /\d/.test(value))) {
    callback(new Error('密码必须包含字母和数字'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, validator: validateUsername, trigger: 'blur' }
  ],
  display_name: [
    { required: true, validator: validateDisplayName, trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  try {
    await registerForm.value.validate();
    loading.value = true;
    
    const requestData = {
      username: form.username,
      display_name: form.display_name,
      password: form.password
    };
    console.log('发送注册请求:', { ...requestData, password: '***' });
    
    // 使用 store 的 register action
    const response = await store.dispatch('register', requestData);
    console.log('注册成功:', response.data);
    
    ElMessage.success('注册成功');
    
    // 确保用户信息已保存后再跳转
    await nextTick();
    router.push('/dashboard');
  } catch (error) {
    console.error('注册失败:', error);
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error);
    } else if (error.message === 'Network Error') {
      ElMessage.error('网络错误，请检查服务器是否正常运行');
    } else {
      ElMessage.error('注册失败，请稍后重试');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="scss" scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
  
  .register-box {
    width: 400px;
    padding: 40px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
    
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
    
    .register-form {
      .submit-btn {
        width: 100%;
        height: 48px;
        padding: 12px;
        font-size: 16px;
      }
      
      :deep(.el-input-group__append) {
        padding: 0 12px;
        color: #909399;
        cursor: pointer;
        
        &:hover {
          color: #409eff;
        }
      }
    }
    
    .login-link {
      margin-top: 16px;
      text-align: center;
      font-size: 14px;
      line-height: 1.5;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      color: #606266;
      
      .el-link {
        font-size: 14px;
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