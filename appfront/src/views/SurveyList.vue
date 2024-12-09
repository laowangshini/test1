<template>
  <div class="survey-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>调查记录列表</span>
          <el-button type="primary" @click="createSurvey">新建调查</el-button>
        </div>
      </template>
      
      <el-table :data="surveys" style="width: 100%">
        <el-table-column prop="name" label="调查名称" />
        <el-table-column prop="start_date" label="开始日期" />
        <el-table-column prop="end_date" label="结束日期" />
        <el-table-column prop="investigator.username" label="调查人" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" @click="viewDetail(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'SurveyList',
  setup() {
    const surveys = ref([])
    const router = useRouter()

    const fetchSurveys = async () => {
      try {
        const response = await axios.get('/api/surveys/')
        surveys.value = response.data
      } catch (error) {
        console.error('获取调查列表失败:', error)
      }
    }

    const viewDetail = (survey) => {
      router.push(`/survey/${survey.id}`)
    }

    const createSurvey = () => {
      router.push('/survey/create')
    }

    onMounted(() => {
      fetchSurveys()
    })

    return {
      surveys,
      viewDetail,
      createSurvey
    }
  }
}
</script> 