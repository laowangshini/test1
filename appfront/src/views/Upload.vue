<template>
  <div class="upload">
    <div class="page-header">
      <h2>上传资料</h2>
    </div>

    <el-card class="upload-form">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="项目标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入项目标题" />
        </el-form-item>

        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述"
          />
        </el-form-item>

        <el-form-item label="项目文件" prop="files">
          <el-upload
            ref="uploadRef"
            class="upload-files"
            action="#"
            :http-request="customUpload"
            :on-remove="handleRemove"
            :before-upload="beforeUpload"
            multiple
            :limit="5"
            :file-list="fileList"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持任意格式文件，单个文件不超过50MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="submitting"
            @click="submitForm"
          >
            提交项目
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 上传提示 -->
    <el-dialog
      v-model="dialogVisible"
      title="提示"
      width="30%"
    >
      <span>项目已提交，等待管理员审核</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="goToProjects">查看项目列表</el-button>
          <el-button type="primary" @click="resetAndClose">
            继续上传
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const formRef = ref(null)
const uploadRef = ref(null)
const fileList = ref([])
const submitting = ref(false)
const dialogVisible = ref(false)

const form = reactive({
  title: '',
  description: '',
  files: []
})

const rules = {
  title: [
    { required: true, message: '请输入项目标题', trigger: 'blur' },
    { min: 3, max: 100, message: '标题长度在3-100个字符之间', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' },
    { min: 10, max: 500, message: '描述长度在10-500个字符之间', trigger: 'blur' }
  ],
  files: [
    { required: true, message: '请上传至少一个文件', trigger: 'change' }
  ]
}

const beforeUpload = (file) => {
  const isLt50M = file.size / 1024 / 1024 < 50
  if (!isLt50M) {
    ElMessage.error('文件大小不能超过50MB!')
    return false
  }
  return true
}

const customUpload = async ({ file }) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await axios.post('/api/files/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    form.files.push(response.data.id)
    ElMessage.success('文件上传成功')
  } catch (error) {
    ElMessage.error('文件上传失败')
    console.error('Upload failed:', error)
  }
}

const handleRemove = (file) => {
  const index = fileList.value.indexOf(file)
  if (index !== -1) {
    fileList.value.splice(index, 1)
    form.files.splice(index, 1)
  }
}

const submitForm = () => {
  if (form.files.length === 0) {
    ElMessage.warning('请至少上传一个文件')
    return
  }

  formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await axios.post('/api/projects/', form)
        dialogVisible.value = true
      } catch (error) {
        ElMessage.error('提交失败')
        console.error('Submit failed:', error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetForm = () => {
  formRef.value.resetFields()
  fileList.value = []
  form.files = []
}

const resetAndClose = () => {
  dialogVisible.value = false
  resetForm()
}

const goToProjects = () => {
  router.push('/projects')
}
</script>

<style lang="scss" scoped>
.upload {
  .page-header {
    margin-bottom: 24px;
    
    h2 {
      margin: 0;
      color: #2c3e50;
      font-size: 24px;
      font-weight: 500;
    }
  }
  
  .upload-form {
    padding: 24px;
    
    .upload-files {
      :deep(.el-upload-list) {
        margin-top: 12px;
      }
      
      :deep(.el-upload__tip) {
        margin-top: 8px;
        color: #909399;
      }
    }
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
}
</style>