<template>
  <div class="contact">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="contact-form-card">
          <template #header>
            <div class="card-header">
              <h3>联系开发者</h3>
            </div>
          </template>
          
          <el-form
            ref="contactForm"
            :model="formData"
            :rules="rules"
            label-width="100px"
          >
            <el-form-item label="问题类型" prop="type">
              <el-select v-model="formData.type" placeholder="请选择问题类型">
                <el-option label="功能建议" value="feature" />
                <el-option label="问题反馈" value="bug" />
                <el-option label="使用咨询" value="usage" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>

            <el-form-item label="标题" prop="title">
              <el-input v-model="formData.title" placeholder="请简要描述您的问题" />
            </el-form-item>

            <el-form-item label="详细描述" prop="content">
              <el-input
                v-model="formData.content"
                type="textarea"
                :rows="6"
                placeholder="请详细描述您的问题或建议"
              />
            </el-form-item>

            <el-form-item label="附件">
              <el-upload
                class="upload-demo"
                action="#"
                :auto-upload="false"
                :on-change="handleFileChange"
                :file-list="formData.files"
              >
                <el-button type="primary">选择文件</el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    可上传截图或相关文档（最大 5MB）
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <el-form-item label="联系方式" prop="contact">
              <el-input
                v-model="formData.contact"
                placeholder="请留下您的联系方式（邮箱/电话）"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="submitForm">提交</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>其他联系方式</h3>
            </div>
          </template>
          
          <div class="contact-info">
            <div class="info-item">
              <el-icon><message /></el-icon>
              <div class="info-content">
                <h4>电子邮箱</h4>
                <p>320220922491@lzu.edu.cn</p>
              </div>
            </div>

            <div class="info-item">
              <el-icon><phone /></el-icon>
              <div class="info-content">
                <h4>服务热线</h4>
                <p>18326466010</p>
                <small>工作日 9:00-18:00</small>
              </div>
            </div>

            <div class="info-item">
              <el-icon><chat-dot-round /></el-icon>
              <div class="info-content">
                <h4>在线客服</h4>
                <el-button type="success" size="small">
                  立即咨询
                </el-button>
              </div>
            </div>

            <el-divider />

            <div class="faq-section">
              <h4>常见问题</h4>
              <el-collapse>
                <el-collapse-item title="如何上传资料？" name="1">
                  <p>点击左侧菜单的"上传资料"，按照提示填写相关信息并上传文件即可。</p>
                </el-collapse-item>
                <el-collapse-item title="支持哪些文件格式？" name="2">
                  <p>系统支持常见的文档格式（PDF、Word、Excel等）、图片格式（JPG、PNG等）和音视频格式。</p>
                </el-collapse-item>
                <el-collapse-item title="如何修改个人信息？" name="3">
                  <p>在"个人设置"中可以修改您的个人信息、密码等设置。</p>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Message,
  Phone,
  ChatDotRound
} from '@element-plus/icons-vue'

const contactForm = ref(null)

const formData = ref({
  type: '',
  title: '',
  content: '',
  contact: '',
  files: []
})

const rules = {
  type: [
    { required: true, message: '请选择问题类型', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 5, max: 50, message: '长度在 5 到 50 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入详细描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  contact: [
    { required: true, message: '请输入联系方式', trigger: 'blur' }
  ]
}

const handleFileChange = (file, fileList) => {
  formData.value.files = fileList
}

const submitForm = async () => {
  if (!contactForm.value) return
  
  await contactForm.value.validate((valid, fields) => {
    if (valid) {
      // TODO: 实现提交逻辑
      ElMessage.success('提交成功，我们会尽快回复您！')
      resetForm()
    } else {
      console.log('验证失败:', fields)
    }
  })
}

const resetForm = () => {
  if (!contactForm.value) return
  contactForm.value.resetFields()
  formData.value.files = []
}
</script>

<style lang="scss" scoped>
.contact {
  .contact-form-card {
    .card-header {
      h3 {
        margin: 0;
        font-size: 18px;
      }
    }
  }

  .info-card {
    .card-header {
      h3 {
        margin: 0;
        font-size: 18px;
      }
    }

    .contact-info {
      .info-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 24px;
        
        .el-icon {
          font-size: 24px;
          color: #409eff;
          margin-right: 16px;
          margin-top: 4px;
        }
        
        .info-content {
          h4 {
            margin: 0 0 8px;
            font-size: 16px;
          }
          
          p {
            margin: 0;
            color: #606266;
          }
          
          small {
            color: #909399;
            font-size: 12px;
          }
        }
      }

      .faq-section {
        h4 {
          margin: 16px 0;
          font-size: 16px;
        }
        
        .el-collapse {
          border: none;
          
          :deep(.el-collapse-item__header) {
            font-size: 14px;
          }
          
          :deep(.el-collapse-item__content) {
            padding: 10px;
            color: #606266;
            font-size: 13px;
          }
        }
      }
    }
  }
}
</style> 