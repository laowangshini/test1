<template>
  <div class="projects">
    <div class="page-header">
      <h2>田野项目</h2>
      <el-input
        v-model="searchQuery"
        placeholder="搜索项目"
        class="search-input"
        :prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
    </div>

    <!-- 项目列表 -->
    <div class="project-list">
      <el-row :gutter="20">
        <el-col :span="8" v-for="project in filteredProjects" :key="project.id">
          <el-card class="project-card" shadow="hover">
            <div class="project-header">
              <h3>{{ project.title }}</h3>
              <el-tag :type="project.status === 'approved' ? 'success' : 'warning'">
                {{ project.status === 'approved' ? '已审核' : '待审核' }}
              </el-tag>
            </div>
            
            <p class="project-description">{{ project.description }}</p>
            
            <div class="project-meta">
              <span class="author">
                <el-icon><user /></el-icon>
                {{ project.author }}
              </span>
              <span class="date">
                <el-icon><calendar /></el-icon>
                {{ formatDate(project.created_at) }}
              </span>
            </div>
            
            <div class="project-stats">
              <span class="likes">
                <el-icon><star /></el-icon>
                {{ project.likes_count }} 赞
              </span>
              <span class="comments">
                <el-icon><chat-dot-round /></el-icon>
                {{ project.comments_count }} 评论
              </span>
              <span class="files">
                <el-icon><document /></el-icon>
                {{ project.files_count }} 文件
              </span>
            </div>
            
            <div class="project-actions">
              <el-button type="primary" @click="viewProject(project.id)">
                查看详情
              </el-button>
              <el-button
                :type="project.is_liked ? 'danger' : 'default'"
                @click="toggleLike(project)"
              >
                <el-icon><star /></el-icon>
                {{ project.is_liked ? '取消赞' : '点赞' }}
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model="currentPage"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[12, 24, 36]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Search,
  User,
  Calendar,
  Star,
  ChatDotRound,
  Document
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const projects = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

const filteredProjects = computed(() => {
  if (!searchQuery.value) return projects.value
  const query = searchQuery.value.toLowerCase()
  return projects.value.filter(project => 
    project.title.toLowerCase().includes(query) ||
    project.description.toLowerCase().includes(query)
  )
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const fetchProjects = async () => {
  try {
    const response = await axios.get('/api/projects/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    projects.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    ElMessage.error('获取项目列表失败')
    console.error('Failed to fetch projects:', error)
  }
}

const toggleLike = async (project) => {
  try {
    await axios.post(`/api/projects/${project.id}/like/`)
    project.is_liked = !project.is_liked
    project.likes_count += project.is_liked ? 1 : -1
    ElMessage.success(project.is_liked ? '点赞成功' : '已取消点赞')
  } catch (error) {
    ElMessage.error('操作失败')
    console.error('Failed to toggle like:', error)
  }
}

const viewProject = (id) => {
  router.push(`/projects/${id}`)
}

const handleSearch = () => {
  currentPage.value = 1
  fetchProjects()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchProjects()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchProjects()
}

onMounted(() => {
  fetchProjects()
})
</script>

<style lang="scss" scoped>
.projects {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    h2 {
      margin: 0;
      color: #2c3e50;
      font-size: 24px;
      font-weight: 500;
    }
    
    .search-input {
      width: 300px;
    }
  }
  
  .project-list {
    margin-bottom: 24px;
    
    .project-card {
      margin-bottom: 20px;
      transition: transform 0.2s;
      
      &:hover {
        transform: translateY(-4px);
      }
      
      .project-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        
        h3 {
          margin: 0;
          font-size: 18px;
          font-weight: 500;
          color: #2c3e50;
        }
      }
      
      .project-description {
        color: #606266;
        font-size: 14px;
        margin-bottom: 16px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .project-meta {
        display: flex;
        gap: 16px;
        margin-bottom: 12px;
        color: #909399;
        font-size: 13px;
        
        span {
          display: flex;
          align-items: center;
          gap: 4px;
        }
      }
      
      .project-stats {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
        color: #909399;
        font-size: 13px;
        
        span {
          display: flex;
          align-items: center;
          gap: 4px;
        }
      }
      
      .project-actions {
        display: flex;
        gap: 12px;
        
        .el-button {
          flex: 1;
        }
      }
    }
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 32px;
  }
}
</style> 