<template>
  <div class="square">
    <!-- 搜索和筛选区域 -->
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索资料..."
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><search /></el-icon>
        </template>
      </el-input>
      
      <el-select
        v-model="selectedType"
        placeholder="资料类型"
        clearable
        @change="handleSearch"
      >
        <el-option label="风土人情" value="FOLKLORE" />
        <el-option label="访谈记录" value="INTERVIEW" />
        <el-option label="文献资料" value="LITERATURE" />
      </el-select>
    </div>

    <!-- 资料列表 -->
    <div class="projects-grid">
      <el-row :gutter="20">
        <el-col 
          v-for="item in filteredProjects" 
          :key="item.id" 
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
        >
          <el-card class="project-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="title">{{ item.title }}</span>
                <el-tag :type="getTypeTag(item.category)">
                  {{ getTypeText(item.category) }}
                </el-tag>
              </div>
            </template>
            
            <div class="card-content">
              <div class="media-preview">
                <!-- 根据文件类型显示不同的预览 -->
                <img 
                  v-if="isImage(item.file_path)" 
                  :src="item.file_path" 
                  alt="预览图"
                />
                <div v-else class="file-icon">
                  <el-icon :size="40">
                    <component :is="getFileIcon(item.file_path)" />
                  </el-icon>
                  <span>{{ getFileType(item.file_path) }}</span>
                </div>
              </div>
              
              <p class="description">{{ item.description || '暂无描述' }}</p>
              
              <div class="meta-info">
                <span class="time">
                  <el-icon><clock /></el-icon>
                  {{ formatDate(item.created_at) }}
                </span>
                <span class="uploader">
                  <el-icon><user /></el-icon>
                  {{ item.investigator?.username || '未知用户' }}
                </span>
              </div>
            </div>
            
            <div class="card-actions">
              <el-button 
                type="primary" 
                link 
                @click="handlePreview(item)"
              >
                查看详情
              </el-button>
              <el-button 
                type="primary" 
                link 
                @click="handleDownload(item)"
              >
                下载
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      :title="currentItem?.title"
      width="70%"
      destroy-on-close
    >
      <div class="preview-content">
        <!-- 图片预览 -->
        <img 
          v-if="isImage(currentItem?.file_path)"
          :src="currentItem?.file_path"
          class="preview-image"
        />
        <!-- PDF预览 -->
        <iframe
          v-else-if="isPDF(currentItem?.file_path)"
          :src="currentItem?.file_path"
          class="preview-pdf"
        ></iframe>
        <!-- 音频预览 -->
        <audio
          v-else-if="isAudio(currentItem?.file_path)"
          controls
          class="preview-audio"
        >
          <source :src="currentItem?.file_path" />
        </audio>
        <!-- 视频预览 -->
        <video
          v-else-if="isVideo(currentItem?.file_path)"
          controls
          class="preview-video"
        >
          <source :src="currentItem?.file_path" />
        </video>
        <!-- 其他文件类型 -->
        <div v-else class="preview-other">
          <el-icon :size="60">
            <component :is="getFileIcon(currentItem?.file_path)" />
          </el-icon>
          <p>此文件类型暂不支持预览，请下载后查看</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import {
  Search,
  Document,
  Picture,
  VideoPlay,
  Headset,
  Files,
  Clock,
  User
} from '@element-plus/icons-vue'
import { formatDate } from '@/utils/date'

const searchQuery = ref('')
const selectedType = ref('')
const projects = ref([])
const previewVisible = ref(false)
const currentItem = ref(null)

// 获取项目列表
const fetchProjects = async () => {
  try {
    const response = await axios.get('/api/surveys/')
    projects.value = response.data
  } catch (error) {
    console.error('获取资料列表失败:', error)
    ElMessage.error('获取资料列表失败')
  }
}

// 过滤后的项目列表
const filteredProjects = computed(() => {
  return projects.value.filter(project => {
    const matchesSearch = !searchQuery.value || 
      project.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      project.description?.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesType = !selectedType.value || project.category === selectedType.value
    
    return matchesSearch && matchesType
  })
})

// 处理搜索
const handleSearch = () => {
  // 搜索逻辑已通过计算属性实现
}

// 文件类型判断函数
const isImage = (path) => {
  if (!path) return false
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(path)
}

const isPDF = (path) => {
  if (!path) return false
  return /\.pdf$/i.test(path)
}

const isAudio = (path) => {
  if (!path) return false
  return /\.(mp3|wav|ogg)$/i.test(path)
}

const isVideo = (path) => {
  if (!path) return false
  return /\.(mp4|webm|ogg)$/i.test(path)
}

// 获取文件图标
const getFileIcon = (path) => {
  if (isImage(path)) return Picture
  if (isPDF(path)) return Document
  if (isAudio(path)) return Headset
  if (isVideo(path)) return VideoPlay
  return Files
}

// 获取文件类型显示文本
const getFileType = (path) => {
  if (isImage(path)) return '图片'
  if (isPDF(path)) return 'PDF'
  if (isAudio(path)) return '音频'
  if (isVideo(path)) return '视频'
  return '文件'
}

// 获取资料类型标签样式
const getTypeTag = (type) => {
  switch (type) {
    case 'FOLKLORE':
      return 'success'
    case 'INTERVIEW':
      return 'warning'
    case 'LITERATURE':
      return 'info'
    default:
      return ''
  }
}

// 获取资料类型显示文本
const getTypeText = (type) => {
  switch (type) {
    case 'FOLKLORE':
      return '风土人情'
    case 'INTERVIEW':
      return '访谈记录'
    case 'LITERATURE':
      return '文献资料'
    default:
      return '未知类型'
  }
}

// 处理预览
const handlePreview = (item) => {
  currentItem.value = item
  previewVisible.value = true
}

// 处理下载
const handleDownload = async (item) => {
  try {
    const response = await axios({
      url: item.file_path,
      method: 'GET',
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', item.title)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('文件下载成功')
  } catch (error) {
    console.error('文件下载失败:', error)
    ElMessage.error('文件下载失败')
  }
}

onMounted(() => {
  fetchProjects()
})
</script>

<style lang="scss" scoped>
.square {
  .filter-section {
    display: flex;
    gap: 20px;
    margin-bottom: 24px;
    
    .search-input {
      width: 300px;
    }
  }
  
  .projects-grid {
    .project-card {
      margin-bottom: 20px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .title {
          font-weight: bold;
          flex: 1;
          margin-right: 12px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
      
      .card-content {
        .media-preview {
          height: 160px;
          display: flex;
          align-items: center;
          justify-content: center;
          background-color: #f5f7fa;
          border-radius: 4px;
          margin-bottom: 12px;
          
          img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
          }
          
          .file-icon {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #909399;
            
            span {
              margin-top: 8px;
              font-size: 14px;
            }
          }
        }
        
        .description {
          font-size: 14px;
          color: #606266;
          margin: 12px 0;
          height: 40px;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
        }
        
        .meta-info {
          display: flex;
          justify-content: space-between;
          font-size: 12px;
          color: #909399;
          
          .time, .uploader {
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
      }
      
      .card-actions {
        margin-top: 12px;
        display: flex;
        justify-content: flex-end;
        gap: 12px;
      }
    }
  }
}

.preview-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  
  .preview-image {
    max-width: 100%;
    max-height: 70vh;
  }
  
  .preview-pdf {
    width: 100%;
    height: 70vh;
    border: none;
  }
  
  .preview-audio {
    width: 100%;
  }
  
  .preview-video {
    max-width: 100%;
    max-height: 70vh;
  }
  
  .preview-other {
    text-align: center;
    color: #909399;
    
    p {
      margin-top: 16px;
    }
  }
}
</style> 