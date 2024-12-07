<template>
  <div class="my-projects">
    <h2>我的项目</h2>
    
    <el-table :data="projects" style="width: 100%">
      <el-table-column prop="title" label="项目名称" />
      <el-table-column prop="start_date" label="开始日期" />
      <el-table-column prop="end_date" label="结束日期" />
      <el-table-column prop="status" label="审核状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button @click="handleEdit(row)" type="primary" size="small">编辑</el-button>
          <el-button @click="handleViewFiles(row)" type="info" size="small">查看文件</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑项目对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑项目" width="50%">
      <el-form :model="editForm" label-width="120px">
        <el-form-item label="项目标题" required>
          <el-input v-model="editForm.title" />
        </el-form-item>
        <el-form-item label="纬度" required>
          <el-input-number v-model="editForm.latitude" :precision="6" />
        </el-form-item>
        <el-form-item label="经度" required>
          <el-input-number v-model="editForm.longitude" :precision="6" />
        </el-form-item>
        <el-form-item label="调查时间段" required>
          <el-date-picker
            v-model="editForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveEdit">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看文件对话框 -->
    <el-dialog v-model="filesDialogVisible" title="项目文件" width="70%">
      <div class="files-grid">
        <div v-for="file in projectFiles" :key="file.id" class="file-item">
          <div class="file-type">{{ getFileTypeText(file.file_type) }}</div>
          <div class="file-title">{{ file.title }}</div>
          <div class="file-status">
            <el-tag :type="getStatusType(file.status)">{{ getStatusText(file.status) }}</el-tag>
          </div>
          <div class="file-actions">
            <a :href="file.file_url" target="_blank">
              <el-button type="primary" size="small">下载</el-button>
            </a>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const projects = ref([])
const editDialogVisible = ref(false)
const filesDialogVisible = ref(false)
const editForm = ref({})
const projectFiles = ref([])

// 获取我的项目列表
const fetchProjects = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/projects/', {
      params: { view_type: 'my' }
    })
    projects.value = response.data
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  }
}

// 获取项目文件
const handleViewFiles = async (project) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/projects/${project.id}/files/`)
    projectFiles.value = response.data
    filesDialogVisible.value = true
  } catch (error) {
    console.error('获��项目文件失败:', error)
    ElMessage.error('获取项目文件失败')
  }
}

// 编辑项目
const handleEdit = (project) => {
  editForm.value = {
    ...project,
    dateRange: [new Date(project.start_date), new Date(project.end_date)]
  }
  editDialogVisible.value = true
}

// 保存编辑
const handleSaveEdit = async () => {
  try {
    const data = {
      ...editForm.value,
      start_date: editForm.value.dateRange[0].toISOString().split('T')[0],
      end_date: editForm.value.dateRange[1].toISOString().split('T')[0],
      status: 'pending'  // 编辑后重置为待审核状态
    }
    delete data.dateRange

    await axios.put(`http://127.0.0.1:8000/api/projects/${editForm.value.id}/`, data)
    ElMessage.success('项目更新成功，等待审核')
    editDialogVisible.value = false
    fetchProjects()
  } catch (error) {
    console.error('更新项目失败:', error)
    ElMessage.error('更新项目失败')
  }
}

// 状态显示相关
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return texts[status] || status
}

const getFileTypeText = (type) => {
  const texts = {
    image: '图片',
    audio: '音频',
    document: '文献'
  }
  return texts[type] || type
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.my-projects {
  padding: 20px;
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

.file-status {
  margin: 5px 0;
}

.file-actions {
  display: flex;
  justify-content: flex-end;
}
</style>