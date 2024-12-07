<template>
  <div class="square">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-input
          v-model="searchQuery"
          placeholder="搜索资料..."
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><component :is="Search" /></el-icon>
          </template>
        </el-input>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="filter-row">
      <el-col :span="24">
        <el-select v-model="selectedType" placeholder="资料类型" class="filter-item" @change="handleFilter">
          <el-option label="全部类型" value="" />
          <el-option label="图片" value="image" />
          <el-option label="音频" value="audio" />
          <el-option label="文献" value="document" />
        </el-select>
        
        <el-select v-model="selectedSort" placeholder="排序方式" class="filter-item" @change="handleFilter">
          <el-option label="最新上传" value="newest" />
          <el-option label="最多收藏" value="likes" />
        </el-select>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="project-list">
      <el-col :span="8" v-for="project in projects" :key="project.id">
        <el-card class="project-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="project-title">{{ project.title }}</span>
              <el-tag size="small" type="success">已审核</el-tag>
            </div>
          </template>
          
          <div class="project-info">
            <div class="meta-info">
              <span>
                <el-icon><Calendar /></el-icon>
                {{ formatDate(project.start_date) }} 至 {{ formatDate(project.end_date) }}
              </span>
              <span>
                <el-icon><Location /></el-icon>
                {{ project.latitude }}, {{ project.longitude }}
              </span>
            </div>
            <div class="stats">
              <span>
                <el-icon><PictureFilled /></el-icon>
                图片: {{ countFilesByType(project.files, 'image') }}
              </span>
              <span>
                <el-icon><Microphone /></el-icon>
                音频: {{ countFilesByType(project.files, 'audio') }}
              </span>
              <span>
                <el-icon><Document /></el-icon>
                文献: {{ countFilesByType(project.files, 'document') }}
              </span>
            </div>
          </div>
          
          <div class="actions">
            <el-button type="primary" size="small" @click="viewFiles(project)">
              查看资料
            </el-button>
            <el-button 
              :type="project.is_liked ? 'danger' : 'default'" 
              size="small" 
              @click="toggleLike(project)"
            >
              {{ project.is_liked ? '取消收藏' : '收藏' }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 查看文件对话框 -->
    <el-dialog v-model="filesDialogVisible" title="项目资料" width="80%" :fullscreen="isFullscreen">
      <template #header="{ close, titleId, titleClass }">
        <div class="dialog-header">
          <h4 :id="titleId" :class="titleClass">项目资料</h4>
          <div class="dialog-actions">
            <el-button @click="toggleFullscreen">
              <el-icon><FullScreen v-if="!isFullscreen" /><Minus v-else /></el-icon>
              {{ isFullscreen ? '退出全屏' : '全屏' }}
            </el-button>
            <el-button @click="close">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
        </div>
      </template>

      <div class="files-container">
        <!-- 文件列表 -->
        <div class="files-list">
          <div v-for="file in currentFiles" 
               :key="file.id" 
               class="file-item"
               :class="{ active: selectedFile?.id === file.id }"
               @click="selectFile(file)">
            <el-icon class="file-icon">
              <component :is="file.file_type === 'image' ? Picture : 
                             file.file_type === 'audio' ? Microphone : 
                             Document" />
            </el-icon>
            <div class="file-info">
              <div class="file-title">{{ file.title }}</div>
              <div class="file-type">{{ getFileTypeText(file.file_type) }}</div>
            </div>
          </div>
        </div>

        <!-- 文件预览区域 -->
        <div class="file-preview" v-if="selectedFile">
          <div class="preview-header">
            <h3>{{ selectedFile.title }}</h3>
            <el-button type="primary" @click="downloadFile(selectedFile)">
              <el-icon><component :is="Download" /></el-icon>
              下载
            </el-button>
          </div>

          <div class="preview-content">
            <!-- 图片预览 -->
            <div v-if="selectedFile.file_type === 'image'" class="image-preview">
              <el-image 
                :src="selectedFile.file_url" 
                :preview-src-list="[selectedFile.file_url]"
                fit="contain"
                :initial-index="0"
                :referrer-policy="'no-referrer'"
                @error="handleImageError"
              >
                <template #placeholder>
                  <div class="image-placeholder">
                    <el-icon class="is-loading">
                      <component :is="Loading" />
                    </el-icon>
                    <p>加载中...</p>
                  </div>
                </template>
                <template #error>
                  <div class="image-error">
                    <el-icon>
                      <component :is="PictureFailed" />
                    </el-icon>
                    <p>图片加载失败</p>
                    <el-button size="small" @click="retryLoadImage">重试</el-button>
                  </div>
                </template>
              </el-image>
            </div>

            <!-- 音频预览 -->
            <div v-else-if="selectedFile.file_type === 'audio'" class="audio-preview">
              <audio 
                controls 
                :src="selectedFile.file_url" 
                style="width: 100%"
                @error="handleAudioError"
              >
                <p>您的浏览器不支持音频播放</p>
              </audio>
            </div>

            <!-- PDF预览 -->
            <div v-else-if="selectedFile.file_type === 'document'" class="pdf-preview">
              <object
                :data="selectedFile.file_url"
                type="application/pdf"
                width="100%"
                height="100%"
              >
                <p>您的浏览器不支持PDF预览，请<a :href="selectedFile.file_url" target="_blank">点击此处</a>下载查看</p>
              </object>
            </div>
          </div>
        </div>

        <!-- 未选择文件时的提示 -->
        <div v-else class="no-file-selected">
          <el-empty description="请选择要预览的文件" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'

// 注册所有图标
const icons = ElementPlusIconsVue
const {
  Calendar,
  Location,
  PictureFilled,
  Microphone,
  Document,
  Search,
  Download,
  FullScreen,
  Minus,
  Close,
  Picture,
  PictureFailed,
  Loading
} = icons

const searchQuery = ref('')
const selectedType = ref('')
const selectedSort = ref('newest')
const projects = ref([])
const filesDialogVisible = ref(false)
const currentFiles = ref([])
const selectedFile = ref(null)
const isFullscreen = ref(false)

// 获取项目列表
const fetchProjects = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/projects/', {
      params: { 
        view_type: 'public',
        search: searchQuery.value,
        file_type: selectedType.value,
        sort: selectedSort.value
      }
    })
    projects.value = response.data
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  }
}

// 选择文件
const selectFile = (file) => {
  console.log('Selected file:', file)  // 添加调试输出
  selectedFile.value = file
  // 预加载文件
  if (file.file_type === 'image') {
    const img = new Image()
    img.src = file.file_url
    console.log('Loading image URL:', file.file_url)  // 添加调试输出
  }
}

// 下载文件
const downloadFile = (file) => {
  try {
    const link = document.createElement('a')
    link.href = file.file_url
    // 从URL中提取文件名
    const fileName = file.file_url.split('/').pop()
    link.download = fileName || file.title
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.success('开始下载文件')
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败')
  }
}

// 切换全屏
const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
}

// 查看文件
const viewFiles = async (project) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/projects/${project.id}/files/`)
    console.log('Files response:', response.data)  // 添加调试输出
    if (response.data && Array.isArray(response.data)) {
      currentFiles.value = response.data
      selectedFile.value = null // 重置选中的文件
      if (currentFiles.value.length === 0) {
        ElMessage.warning('该项目暂无文件')
      } else {
        filesDialogVisible.value = true
      }
    } else {
      ElMessage.error('获取文件列表失败')
    }
  } catch (error) {
    console.error('获取文件列表失败:', error)
    if (error.response?.status === 403) {
      ElMessage.warning('项目未审核通过，暂时无法查看文件')
    } else {
      ElMessage.error('获取文件列表失败')
    }
  }
}

// 收藏/取消收藏
const toggleLike = async (project) => {
  try {
    await axios.post(`http://127.0.0.1:8000/api/projects/${project.id}/like/`)
    project.is_liked = !project.is_liked
    ElMessage.success(project.is_liked ? '收藏成功' : '已取消收藏')
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 处理搜索
const handleSearch = () => {
  fetchProjects()
}

// 处理筛选
const handleFilter = () => {
  fetchProjects()
}

// 辅助函数
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const countFilesByType = (files, type) => {
  return files.filter(file => file.file_type === type).length
}

const getFileTypeText = (type) => {
  const texts = {
    image: '图片',
    audio: '音频',
    document: '文献'
  }
  return texts[type] || type
}

// 重试加载图片
const retryLoadImage = () => {
  if (selectedFile.value) {
    const img = new Image()
    img.src = selectedFile.value.file_url + '?t=' + new Date().getTime()
    img.onload = () => {
      // 强制刷新图片
      selectedFile.value = { ...selectedFile.value }
    }
    img.onerror = () => {
      console.error('重试加载图片失败:', selectedFile.value.file_url)
      ElMessage.error('重试加载图片失败')
    }
  }
}

// 文件预览错误处理
const handleImageError = () => {
  console.error('图片加载失败:', selectedFile.value?.file_url)
  ElMessage.error('图片加载失败')
  // 可以在这里添加重试逻辑
}

const handleAudioError = () => {
  console.error('音频加载失败:', selectedFile.value?.file_url)
  ElMessage.error('音频加载失败')
}

const handlePdfError = () => {
  console.error('PDF加载失败:', selectedFile.value?.file_url)
  ElMessage.error('PDF加载失败')
}

onMounted(() => {
  fetchProjects()
})
</script>

<style lang="scss" scoped>
.square {
  padding: 20px;

  .search-input {
    margin-bottom: 20px;
  }

  .filter-row {
    margin-bottom: 20px;
    
    .filter-item {
      margin-right: 16px;
      width: 160px;
    }
  }

  .project-list {
    margin-bottom: 20px;
    
    .project-card {
      margin-bottom: 20px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .project-title {
          font-weight: bold;
          flex: 1;
          margin-right: 12px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
      
      .project-info {
        .meta-info {
          display: flex;
          flex-direction: column;
          gap: 8px;
          color: #666;
          font-size: 13px;
          margin: 12px 0;
          
          span {
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
        
        .stats {
          display: flex;
          justify-content: space-around;
          color: #666;
          font-size: 13px;
          margin: 16px 0;
          
          span {
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
      }
      
      .actions {
        display: flex;
        justify-content: space-between;
        margin-top: 16px;
      }
    }
  }

  .files-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }

  .file-item {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .file-type {
    font-weight: bold;
    color: #666;
  }

  .file-title {
    font-size: 16px;
  }

  .file-actions {
    display: flex;
    justify-content: flex-end;
  }
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;

  h4 {
    margin: 0;
    font-size: 18px;
  }

  .dialog-actions {
    display: flex;
    gap: 10px;
  }
}

.files-container {
  display: flex;
  height: calc(100vh - 200px);
  gap: 20px;
}

.files-list {
  width: 300px;
  border-right: 1px solid #eee;
  overflow-y: auto;
  padding: 10px;

  .file-item {
    display: flex;
    align-items: center;
    padding: 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
    gap: 10px;

    &:hover {
      background-color: #f5f7fa;
    }

    &.active {
      background-color: #ecf5ff;
    }

    .file-icon {
      font-size: 24px;
      color: #909399;
    }

    .file-info {
      flex: 1;
      min-width: 0;

      .file-title {
        font-weight: 500;
        margin-bottom: 4px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .file-type {
        font-size: 12px;
        color: #909399;
      }
    }
  }
}

.file-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;

  .preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #eee;

    h3 {
      margin: 0;
      font-size: 16px;
    }
  }

  .preview-content {
    flex: 1;
    padding: 20px;
    overflow: auto;
    background-color: #f5f7fa;

    .image-preview {
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #fff;
      border-radius: 4px;
      box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);

      .el-image {
        max-height: 100%;
        max-width: 100%;
      }
    }

    .audio-preview {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 20px;
      background-color: #fff;
      border-radius: 4px;
      box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);

      audio {
        width: 100%;
        max-width: 500px;
      }
    }

    .pdf-preview {
      height: 100%;
      background-color: #fff;
      border-radius: 4px;
      box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
      overflow: hidden;

      iframe {
        border: none;
      }
    }
  }
}

.no-file-selected {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;

  .el-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }

  p {
    margin: 0;
  }
}
</style> 