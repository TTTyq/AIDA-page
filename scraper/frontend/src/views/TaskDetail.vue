<template>
  <div class="task-detail" v-loading="loading">
    <div v-if="task">
      <el-page-header @back="goBack" :title="'返回任务列表'" :content="task.name" />
      
      <el-row :gutter="20" class="mt-20">
        <el-col :span="16">
          <el-card>
            <template #header>
              <div class="card-header">
                <h2>任务详情</h2>
                <div>
                  <el-button 
                    type="success" 
                    :disabled="task.status === 'running'"
                    @click="runTask"
                  >
                    运行任务
                  </el-button>
                  <el-button 
                    type="primary" 
                    @click="viewData"
                  >
                    查看数据
                  </el-button>
                </div>
              </div>
            </template>
            
            <el-descriptions :column="2" border>
              <el-descriptions-item label="ID">{{ task.id }}</el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="getStatusType(task.status)">
                  {{ getStatusText(task.status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="名称">{{ task.name }}</el-descriptions-item>
              <el-descriptions-item label="URL">{{ task.url }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ formatDate(task.created_at) }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{ task.updated_at ? formatDate(task.updated_at) : '-' }}</el-descriptions-item>
              <el-descriptions-item label="描述" :span="2">{{ task.description || '无描述' }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <h2>爬虫配置</h2>
              </div>
            </template>
            
            <el-descriptions direction="vertical" :column="1" border>
              <el-descriptions-item label="CSS选择器">{{ task.config.selector }}</el-descriptions-item>
              <el-descriptions-item label="使用浏览器">
                <el-tag size="small" :type="task.config.use_browser ? 'success' : 'info'">
                  {{ task.config.use_browser ? '是' : '否' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item v-if="task.config.use_browser" label="等待时间">
                {{ task.config.wait_time }} 秒
              </el-descriptions-item>
              <el-descriptions-item label="启用分页">
                <el-tag size="small" :type="task.config.pagination ? 'success' : 'info'">
                  {{ task.config.pagination ? '是' : '否' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item v-if="task.config.pagination" label="最大页数">
                {{ task.config.max_pages }} 页
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
          
          <el-card class="mt-20">
            <template #header>
              <div class="card-header">
                <h2>数据统计</h2>
              </div>
            </template>
            
            <div class="data-stats">
              <div class="stat-item">
                <div class="stat-value">{{ dataCount }}</div>
                <div class="stat-label">数据条数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ task.status === 'completed' ? '成功' : '-' }}</div>
                <div class="stat-label">爬取结果</div>
              </div>
            </div>
            
            <div class="export-section">
              <h3>导出数据</h3>
              <el-button @click="exportData('json')">导出JSON</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <el-empty v-else description="未找到任务信息" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'TaskDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      dataCount: 0
    }
  },
  computed: {
    ...mapGetters(['isLoading', 'currentTask', 'taskData']),
    loading() {
      return this.isLoading
    },
    task() {
      return this.currentTask
    }
  },
  methods: {
    ...mapActions(['fetchTask', 'fetchTaskData', 'runScraper', 'exportData']),
    getStatusType(status) {
      const types = {
        'pending': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger'
      }
      return types[status] || 'info'
    },
    getStatusText(status) {
      const texts = {
        'pending': '等待中',
        'running': '运行中',
        'completed': '已完成',
        'failed': '失败'
      }
      return texts[status] || status
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString()
    },
    goBack() {
      this.$router.push('/tasks')
    },
    async runTask() {
      try {
        await this.runScraper(this.task.config)
        this.$message.success('任务运行成功')
        this.fetchTask(this.id) // 刷新任务信息
        this.loadTaskData()
      } catch (error) {
        this.$message.error('任务运行失败: ' + error.message)
      }
    },
    viewData() {
      this.$router.push(`/data/${this.id}`)
    },
    async exportDataFile(format) {
      try {
        await this.exportData({
          taskId: this.id,
          format
        })
        this.$message.success(`数据已导出为${format.toUpperCase()}格式`)
      } catch (error) {
        this.$message.error('导出失败: ' + error.message)
      }
    },
    async loadTaskData() {
      await this.fetchTaskData(this.id)
      this.dataCount = this.taskData.length
    }
  },
  async created() {
    await this.fetchTask(this.id)
    this.loadTaskData()
  }
}
</script>

<style scoped>
.task-detail {
  padding: 20px 0;
}

.mt-20 {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
}

.data-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.export-section {
  border-top: 1px solid #EBEEF5;
  padding-top: 15px;
  margin-top: 15px;
}

.export-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}
</style> 