<template>
  <div class="settings">
    <el-tabs v-model="activeTab" class="setting-tabs">
      <el-tab-pane label="基本信息" name="basic">
        <el-form
          ref="basicForm"
          :model="basicInfo"
          :rules="basicRules"
          label-width="100px"
          class="setting-form"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="basicInfo.username" disabled />
          </el-form-item>

          <el-form-item label="显示名称" prop="displayName">
            <el-input v-model="basicInfo.displayName" />
          </el-form-item>

          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="basicInfo.email" />
          </el-form-item>

          <el-form-item label="个人简介" prop="bio">
            <el-input
              v-model="basicInfo.bio"
              type="textarea"
              :rows="4"
              placeholder="请输入个人简介"
            />
          </el-form-item>

          <el-form-item label="所属机构" prop="organization">
            <el-input v-model="basicInfo.organization" />
          </el-form-item>

          <el-form-item label="研究领域" prop="researchFields">
            <el-select
              v-model="basicInfo.researchFields"
              multiple
              filterable
              allow-create
              default-first-option
              placeholder="请选择或输入研究领域"
            >
              <el-option
                v-for="field in researchFieldOptions"
                :key="field"
                :label="field"
                :value="field"
              />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveBasicInfo">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="安全设置" name="security">
        <el-form
          ref="passwordForm"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="100px"
          class="setting-form"
        >
          <el-form-item label="当前密码" prop="currentPassword">
            <el-input
              v-model="passwordForm.currentPassword"
              type="password"
              show-password
            />
          </el-form-item>

          <el-form-item label="新密码" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              show-password
            />
          </el-form-item>

          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="changePassword">修改密码</el-button>
          </el-form-item>
        </el-form>

        <el-divider />

        <div class="security-section">
          <h3>账号安全</h3>
          <div class="security-item">
            <div class="security-info">
              <span class="label">双因素认证</span>
              <span class="status">未开启</span>
            </div>
            <el-button type="primary" plain>开启</el-button>
          </div>
          <div class="security-item">
            <div class="security-info">
              <span class="label">登录设备管理</span>
              <span class="status">3 台设备</span>
            </div>
            <el-button type="primary" plain>查看</el-button>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="通知设置" name="notification">
        <div class="notification-section">
          <h3>邮件通知</h3>
          <el-form label-width="200px" class="setting-form">
            <el-form-item label="资料被下载时通知">
              <el-switch v-model="notifications.downloadNotify" />
            </el-form-item>
            <el-form-item label="收到新评论时通知">
              <el-switch v-model="notifications.commentNotify" />
            </el-form-item>
            <el-form-item label="项目被收藏时通知">
              <el-switch v-model="notifications.likeNotify" />
            </el-form-item>
            <el-form-item label="系统公告">
              <el-switch v-model="notifications.systemNotify" />
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('basic')

// 基本信息
const basicInfo = ref({
  username: 'user123',
  displayName: '张三',
  email: 'zhangsan@example.com',
  bio: '人类学研究者，专注于少数民族文化研究。',
  organization: '某某大学人类学系',
  researchFields: ['文化人类学', '民族志']
})

const researchFieldOptions = [
  '文化人类学',
  '民族志',
  '体质人类学',
  '语言人类学',
  '考古人类学',
  '民族学',
  '社会学'
]

const basicRules = {
  displayName: [
    { required: true, message: '请输入显示名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  bio: [
    { max: 200, message: '不能超过 200 个字符', trigger: 'blur' }
  ],
  organization: [
    { required: true, message: '请输入所属机构', trigger: 'blur' }
  ]
}

// 密码表单
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 通知设置
const notifications = ref({
  downloadNotify: true,
  commentNotify: true,
  likeNotify: true,
  systemNotify: true
})

// 保存基本信息
const saveBasicInfo = async () => {
  // TODO: 实现保存逻辑
  ElMessage.success('基本信息已更新')
}

// 修改密码
const changePassword = async () => {
  // TODO: 实现修改密码逻辑
  ElMessage.success('密码已修改')
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}
</script>

<style lang="scss" scoped>
.settings {
  .setting-tabs {
    .setting-form {
      max-width: 600px;
      margin-top: 20px;
    }
  }

  .security-section {
    margin-top: 20px;
    
    h3 {
      margin-bottom: 16px;
      font-size: 16px;
    }
    
    .security-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 0;
      border-bottom: 1px solid #ebeef5;
      
      &:last-child {
        border-bottom: none;
      }
      
      .security-info {
        .label {
          font-size: 14px;
          margin-right: 12px;
        }
        
        .status {
          color: #909399;
          font-size: 13px;
        }
      }
    }
  }

  .notification-section {
    margin-top: 20px;
    
    h3 {
      margin-bottom: 24px;
      font-size: 16px;
    }
  }
}
</style> 