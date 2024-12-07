<template>
  <div class="upload-project">
    <!-- 步骤指示器 -->
    <el-steps :active="currentStep" finish-status="success" class="steps">
      <el-step title="项目信息"></el-step>
      <el-step title="资料上传"></el-step>
    </el-steps>

    <!-- 步骤1：项目基本信息 -->
    <div v-if="currentStep === 0" class="step-container">
      <h2>创建新项目</h2>
      <el-form :model="projectForm" label-width="120px" class="project-form">
        <el-form-item label="项目标题" required>
          <el-input v-model="projectForm.title" placeholder="例如：2024夏,林芝扎嘎乡"/>
        </el-form-item>
        <el-form-item label="纬度" required>
          <el-input-number v-model="projectForm.latitude" :precision="6"/>
        </el-form-item>
        <el-form-item label="经度" required>
          <el-input-number v-model="projectForm.longitude" :precision="6"/>
        </el-form-item>
        <el-form-item label="调查时间段" required>
          <el-date-picker
            v-model="projectForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createProject">下一步</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 步骤2：资料上传 -->
    <div v-if="currentStep === 1" class="step-container">
      <div class="step-header">
        <h2>上传项目资料</h2>
        <el-button @click="prevStep">返回上一步</el-button>
      </div>
      
      <div class="upload-grid">
        <!-- 风土人情和文物照片 -->
        <div class="upload-section">
          <div class="section-header">
            <el-icon><Picture /></el-icon>
            <h3>风土人情和文物照片</h3>
          </div>
          <el-upload
            :action="'http://127.0.0.1:8000/api/files/upload/'"
            :headers="uploadHeaders"
            :data="{
              project: createdProjectId,
              file_type: 'image',
              title: '风土人情和文物照片'
            }"
            :accept="'.jpg,.jpeg,.png'"
            multiple
            list-type="picture-card"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
          <div class="el-upload__tip">支持 jpg/png 格式图片</div>
        </div>

        <!-- 访谈记录 -->
        <div class="upload-section">
          <div class="section-header">
            <el-icon><Microphone /></el-icon>
            <h3>访谈记录</h3>
          </div>
          <el-upload
            :action="'http://127.0.0.1:8000/api/files/upload/'"
            :headers="uploadHeaders"
            :data="{
              project: createdProjectId,
              file_type: 'audio',
              title: '访谈记录'
            }"
            :accept="'.mp3,.mp4'"
            multiple
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon>
              <span>上传访谈</span>
            </el-button>
          </el-upload>
          <div class="el-upload__tip">支持 mp3/mp4 格式文件</div>
        </div>

        <!-- 数字文献 -->
        <div class="upload-section">
          <div class="section-header">
            <el-icon><Document /></el-icon>
            <h3>数字文献</h3>
          </div>
          <el-upload
            :action="'http://127.0.0.1:8000/api/files/upload/'"
            :headers="uploadHeaders"
            :data="{
              project: createdProjectId,
              file_type: 'document',
              title: '数字文献'
            }"
            :accept="'.pdf'"
            multiple
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon>
              <span>上传文献</span>
            </el-button>
          </el-upload>
          <div class="el-upload__tip">支持 PDF 格式文件</div>
        </div>
      </div>

      <div class="step-footer">
        <el-button type="primary" @click="finishUpload">完成上传</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture, Microphone, Document, Upload, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const currentStep = ref(0)
const createdProjectId = ref(null)

const projectForm = ref({
  title: '',
  latitude: null,
  longitude: null,
  dateRange: []
})

const uploadHeaders = {
  'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)?.[1] || ''
}

const createProject = async () => {
  if (!projectForm.value.title || !projectForm.value.latitude || 
      !projectForm.value.longitude || !projectForm.value.dateRange) {
    ElMessage.error('请填写所有必填项')
    return
  }

  try {
    const projectData = {
      title: projectForm.value.title,
      latitude: projectForm.value.latitude,
      longitude: projectForm.value.longitude,
      start_date: projectForm.value.dateRange[0].toISOString().split('T')[0],
      end_date: projectForm.value.dateRange[1].toISOString().split('T')[0]
    };
    
    console.log('发送请求:', projectData);
    
    const response = await axios.post(
      'http://127.0.0.1:8000/api/projects/',
      projectData,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    );
    
    console.log('项目创建成功:', response.data);
    createdProjectId.value = response.data.id;
    currentStep.value = 1;
    ElMessage.success('项目创建成功，请上传资料');
  } catch (error) {
    console.error('项目创建失败:', error);
    ElMessage.error(error.response?.data?.detail || '创建项目失败');
  }
}

const handleUploadSuccess = (response, file) => {
  console.log('文件上传成功:', response)
  ElMessage.success(`${file.name} 上传成功`)
}

const handleUploadError = (error) => {
  console.error('文件上传失败:', error)
  ElMessage.error('文件上传失败')
}

const prevStep = () => {
  currentStep.value--
}

const finishUpload = () => {
  ElMessage.success('项目上传完成')
  currentStep.value = 0
  projectForm.value = {
    title: '',
    latitude: null,
    longitude: null,
    dateRange: []
  }
  createdProjectId.value = null
}
</script>

<style scoped>
.upload-project {
  padding: 20px;
}

.steps {
  margin-bottom: 40px;
}

.step-container {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
}

.project-form {
  max-width: 600px;
  margin: 0 auto;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.upload-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.upload-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.section-header .el-icon {
  margin-right: 8px;
  font-size: 24px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.el-upload__tip {
  margin-top: 8px;
  color: #666;
}

.step-footer {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

:deep(.el-upload--picture-card) {
  width: 148px;
  height: 148px;
  line-height: 148px;
}

h2 {
  margin-top: 0;
  margin-bottom: 24px;
  color: #333;
  font-size: 24px;
}
</style>
 