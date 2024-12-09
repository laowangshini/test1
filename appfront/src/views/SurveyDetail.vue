<template>
  <div class="survey-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ survey.name }}</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="调查时间">
          {{ survey.start_date }} 至 {{ survey.end_date }}
        </el-descriptions-item>
        <el-descriptions-item label="调查人">
          {{ survey.investigator?.username }}
        </el-descriptions-item>
        <el-descriptions-item label="位置">
          经度: {{ survey.longitude }}, 纬度: {{ survey.latitude }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="media-sections">
        <el-tabs>
          <el-tab-pane label="风土人情">
            <media-grid :items="folkloreItems" />
          </el-tab-pane>
          <el-tab-pane label="访谈记录">
            <media-grid :items="interviewItems" />
          </el-tab-pane>
          <el-tab-pane label="文献资料">
            <media-grid :items="literatureItems" />
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import MediaGrid from '@/components/MediaGrid.vue'

export default {
  name: 'SurveyDetail',
  components: { MediaGrid },
  setup() {
    const route = useRoute()
    const survey = ref({})
    
    const folkloreItems = computed(() => 
      survey.value.media_items?.filter(item => item.category === 'FOLKLORE') || []
    )
    
    const interviewItems = computed(() => 
      survey.value.media_items?.filter(item => item.category === 'INTERVIEW') || []
    )
    
    const literatureItems = computed(() => 
      survey.value.media_items?.filter(item => item.category === 'LITERATURE') || []
    )

    const fetchSurveyDetail = async () => {
      try {
        const response = await axios.get(`/api/surveys/${route.params.id}/`)
        survey.value = response.data
      } catch (error) {
        console.error('获取调查详情失败:', error)
      }
    }

    onMounted(() => {
      fetchSurveyDetail()
    })

    return {
      survey,
      folkloreItems,
      interviewItems,
      literatureItems
    }
  }
}
</script> 