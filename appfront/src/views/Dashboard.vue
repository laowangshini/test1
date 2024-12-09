<template>
  <div class="dashboard">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header height="72px">
        <div class="header-left">
          <div class="logo-container">
            <img src="@/assets/logo.png" alt="AnthroHub" class="logo" />
            <span class="logo-text">AnthroHub</span>
          </div>
        </div>
        <div class="header-right">
          <div class="welcome-text">
            尊敬的 <span class="user-name">{{ displayName }}</span> 用户，
            欢迎来到 AnthroHub
            <el-tag size="small" :type="userTypeTag" class="user-type-tag">
              {{ userTypeText }}
            </el-tag>
          </div>
          <el-button type="danger" plain size="default" @click="handleLogout">
            <el-icon><switch-button /></el-icon>
            退出登录
          </el-button>
        </div>
      </el-header>
      
      <el-container class="main-container">
        <!-- 侧边栏 -->
        <el-aside width="260px">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical"
            @select="handleSelect"
          >
            <el-menu-item index="square">
              <el-icon><grid /></el-icon>
              <template #title>
                <span>资料广场</span>
              </template>
            </el-menu-item>
            
            <el-menu-item 
              index="upload"
              :disabled="store.getters.isGuest"
            >
              <el-icon><upload-filled /></el-icon>
              <template #title>
                <span>上传资料</span>
              </template>
            </el-menu-item>
            
            <el-menu-item 
              index="my-projects"
              :disabled="store.getters.isGuest"
            >
              <el-icon><folder-opened /></el-icon>
              <template #title>
                <span>我的项目</span>
              </template>
            </el-menu-item>

            <el-menu-item 
              index="statistics"
              :disabled="store.getters.isGuest"
            >
              <el-icon><trend-charts /></el-icon>
              <template #title>
                <span>统计图表</span>
              </template>
            </el-menu-item>

            <el-menu-item 
              index="settings"
              :disabled="store.getters.isGuest"
            >
              <el-icon><setting /></el-icon>
              <template #title>
                <span>个人设置</span>
              </template>
            </el-menu-item>

            <el-menu-item 
              index="contact"
              :disabled="store.getters.isGuest"
            >
              <el-icon><message /></el-icon>
              <template #title>
                <span>联系开发者</span>
              </template>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- 主内容区 -->
        <el-main>
          <div class="content-container">
            <el-card class="content-card">
              <template #header>
                <div class="content-header">
                  <h2>{{ getContentTitle }}</h2>
                </div>
              </template>
              
              <div class="content-body">
                <component :is="currentComponent" />
              </div>
            </el-card>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, shallowRef, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Grid,
  UploadFilled,
  FolderOpened,
  TrendCharts,
  Setting,
  Message,
  SwitchButton
} from '@element-plus/icons-vue'

// 导入各个组件
import Square from '@/components/Square.vue'
import Upload from '@/components/Upload.vue'
import MyProjects from '@/components/MyProjects.vue'
import Statistics from '@/components/Statistics.vue'
import Settings from '@/components/Settings.vue'
import Contact from '@/components/Contact.vue'

const router = useRouter()
const store = useStore()
const activeMenu = ref('square')

// 组件映射
const componentMap = {
  square: Square,
  upload: Upload,
  'my-projects': MyProjects,
  statistics: Statistics,
  settings: Settings,
  contact: Contact
}

// 标题映射
const titleMap = {
  square: '资料广场',
  upload: '上传资料',
  'my-projects': '我的项目',
  statistics: '统计图表',
  settings: '个人设置',
  contact: '联系开发者'
}

// 当前组件
const currentComponent = shallowRef(Square)

// 获取当前内容标题
const getContentTitle = computed(() => {
  return titleMap[activeMenu.value] || '资料广场'
})

// 从 store 获取用户信息
const displayName = computed(() => {
  const user = store.getters.currentUser
  return user ? user.display_name || user.username : ''
})

const userType = computed(() => {
  const user = store.getters.currentUser
  return user ? user.user_type : ''
})

const userTypeText = computed(() => {
  switch (userType.value) {
    case 'admin':
      return '管理员'
    case 'user':
      return '普通用户'
    default:
      return '未知'
  }
})

const userTypeTag = computed(() => {
  switch (userType.value) {
    case 'admin':
      return 'danger'
    case 'user':
      return 'success'
    default:
      return 'info'
  }
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await store.dispatch('logout')
    router.push('/login')
    ElMessage.success('已安全退出登录')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('退出登录失败:', error)
      ElMessage.error('退出登录失败，请稍后重试')
    }
  }
}

const handleSelect = (index) => {
  // 检查是否有权访问
  if (!store.getters.canAccess(index)) {
    ElMessage.warning('请先登录后再使用此功能');
    // 保持当前选中状态不变
    activeMenu.value = 'square';
    return;
  }
  
  activeMenu.value = index;
  currentComponent.value = componentMap[index];
}

// 确保游客模式下默认选中资料广场
onMounted(() => {
  if (store.getters.isGuest) {
    activeMenu.value = 'square';
    currentComponent.value = componentMap.square;
  }
});
</script>

<style lang="scss" scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f7fa;

  .el-header {
    background-color: white;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    
    .header-left {
      .logo-container {
        display: flex;
        align-items: center;
        gap: 140px;
        
        .logo {
          height: 70px;
          width: auto;
          object-fit: contain;
        }

        .logo-text {
          font-size: 32px;
          font-weight: 600;
          color: #2c3e50;
          letter-spacing: 1.5px;
          font-family: 'Helvetica Neue', Arial, sans-serif;
          margin-left: 24px;
        }
      }
    }
    
    .header-right {
      display: flex;
      align-items: center;
      gap: 24px;
      
      .welcome-text {
        font-size: 15px;
        color: #606266;
        
        .user-name {
          color: #409eff;
          font-weight: 600;
          margin: 0 4px;
        }

        .user-type-tag {
          margin-left: 8px;
        }
      }
    }
  }
  
  .main-container {
    height: calc(100vh - 72px);
    
    .el-aside {
      background-color: white;
      border-right: 1px solid #e6e6e6;
      padding: 20px 0;
      
      .el-menu {
        border-right: none;
        
        .el-menu-item, .el-sub-menu__title {
          height: 56px;
          line-height: 56px;
          padding: 0 24px;
          
          &:hover {
            background-color: #ecf5ff;
          }
          
          .el-icon {
            font-size: 20px;
            margin-right: 12px;
          }
        }
        
        .el-menu-item.is-active {
          background-color: #ecf5ff;
          color: #409eff;
          font-weight: 600;
          
          &::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background-color: #409eff;
          }
        }
      }
    }
    
    .el-main {
      padding: 24px;
      background-color: #f5f7fa;
      overflow-y: auto;
      
      .content-container {
        max-width: 1200px;
        margin: 0 auto;
        
        .content-card {
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
          
          .content-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-bottom: 1px solid #ebeef5;
            
            h2 {
              margin: 0;
              font-size: 18px;
              font-weight: 600;
              color: #303133;
            }
          }
          
          .content-body {
            padding: 20px;
            min-height: 500px;
          }
        }
      }
    }
  }
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 