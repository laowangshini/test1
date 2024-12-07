<template>
  <div class="statistics">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="overview-card">
          <template #header>
            <div class="card-header">
              <h3>数据概览</h3>
              <el-select v-model="timeRange" size="small">
                <el-option label="最近7天" value="7days" />
                <el-option label="最近30天" value="30days" />
                <el-option label="最近3个月" value="3months" />
                <el-option label="最近1年" value="1year" />
              </el-select>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon upload">
                  <el-icon><upload-filled /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.uploads }}</div>
                  <div class="stat-label">上传资料</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon view">
                  <el-icon><view /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.views }}</div>
                  <div class="stat-label">总浏览量</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon download">
                  <el-icon><download /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.downloads }}</div>
                  <div class="stat-label">总下载量</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-icon like">
                  <el-icon><star /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.likes }}</div>
                  <div class="stat-label">收藏数量</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <h3>资料类型分布</h3>
            </div>
          </template>
          <div class="chart-container" ref="pieChartRef"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <h3>数据趋势</h3>
            </div>
          </template>
          <div class="chart-container" ref="lineChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <h3>热门资料排行</h3>
              <el-radio-group v-model="rankType" size="small">
                <el-radio-button label="views">浏览量</el-radio-button>
                <el-radio-button label="downloads">下载量</el-radio-button>
                <el-radio-button label="likes">收藏数</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container" ref="barChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { UploadFilled, View, Download, Star } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const timeRange = ref('7days')
const rankType = ref('views')
const pieChartRef = ref(null)
const lineChartRef = ref(null)
const barChartRef = ref(null)
let pieChart = null
let lineChart = null
let barChart = null

// 模拟数据
const stats = ref({
  uploads: 126,
  views: 3842,
  downloads: 892,
  likes: 456
})

// 初始化饼图
const initPieChart = () => {
  if (pieChartRef.value) {
    pieChart = echarts.init(pieChartRef.value)
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center'
      },
      series: [
        {
          type: 'pie',
          radius: ['50%', '70%'],
          avoidLabelOverlap: false,
          label: {
            show: false
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 'bold'
            }
          },
          data: [
            { value: 45, name: '田野笔记' },
            { value: 25, name: '调查问卷' },
            { value: 20, name: '访谈记录' },
            { value: 10, name: '照片影像' }
          ]
        }
      ]
    }
    pieChart.setOption(option)
  }
}

// 初始化折线图
const initLineChart = () => {
  if (lineChartRef.value) {
    lineChart = echarts.init(lineChartRef.value)
    const option = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['浏览量', '下载量']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '浏览量',
          type: 'line',
          smooth: true,
          data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
          name: '下载量',
          type: 'line',
          smooth: true,
          data: [45, 52, 38, 54, 35, 85, 78]
        }
      ]
    }
    lineChart.setOption(option)
  }
}

// 初始化柱状图
const initBarChart = () => {
  if (barChartRef.value) {
    barChart = echarts.init(barChartRef.value)
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value'
      },
      yAxis: {
        type: 'category',
        data: ['项目1', '项目2', '项目3', '项目4', '项目5']
      },
      series: [
        {
          type: 'bar',
          data: [320, 280, 250, 220, 190]
        }
      ]
    }
    barChart.setOption(option)
  }
}

// 监听窗口大小变化
const handleResize = () => {
  pieChart?.resize()
  lineChart?.resize()
  barChart?.resize()
}

onMounted(() => {
  // 确保 DOM 已经渲染完成
  nextTick(() => {
    initPieChart()
    initLineChart()
    initBarChart()
    window.addEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  pieChart?.dispose()
  lineChart?.dispose()
  barChart?.dispose()
})
</script>

<style lang="scss" scoped>
.statistics {
  .overview-card {
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      h3 {
        margin: 0;
      }
    }
    
    .stat-item {
      display: flex;
      align-items: center;
      padding: 20px;
      
      .stat-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
        
        .el-icon {
          font-size: 24px;
          color: white;
        }
        
        &.upload {
          background-color: #409eff;
        }
        
        &.view {
          background-color: #67c23a;
        }
        
        &.download {
          background-color: #e6a23c;
        }
        
        &.like {
          background-color: #f56c6c;
        }
      }
      
      .stat-info {
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          line-height: 1;
          margin-bottom: 8px;
        }
        
        .stat-label {
          color: #909399;
          font-size: 14px;
        }
      }
    }
  }
  
  .chart-row {
    margin-bottom: 20px;
    
    .chart-card {
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        h3 {
          margin: 0;
        }
      }
      
      .chart-container {
        height: 300px;
      }
    }
  }
}
</style> 