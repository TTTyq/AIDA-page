<template>
  <div class="home">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h2>欢迎使用 AIDA 爬虫工具</h2>
        </div>
      </template>
      <div class="card-content">
        <p>这是一个轻量级的爬虫工具，用于AIDA项目数据采集。</p>
        <div class="quick-actions">
          <el-button type="primary" @click="$router.push('/tasks/new')">
            创建新任务
          </el-button>
          <el-button @click="$router.push('/tasks')">
            查看任务列表
          </el-button>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card">
          <h3>任务总数</h3>
          <div class="stat-number">{{ taskCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <h3>已完成任务</h3>
          <div class="stat-number">{{ completedTaskCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <h3>数据总量</h3>
          <div class="stat-number">{{ dataCount }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="recent-tasks">
      <template #header>
        <div class="card-header">
          <h2>最近任务</h2>
          <el-button text @click="$router.push('/tasks')">查看全部</el-button>
        </div>
      </template>
      <el-table :data="recentTasks" style="width: 100%">
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="url" label="URL" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button text @click="$router.push(`/tasks/${scope.row.id}`)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      // 模拟数据
      taskCount: 0,
      completedTaskCount: 0,
      dataCount: 0,
      recentTasks: []
    }
  },
  computed: {
    ...mapGetters(['allTasks'])
  },
  methods: {
    ...mapActions(['fetchTasks']),
    getStatusType(status) {
      const types = {
        'pending': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger'
      }
      return types[status] || 'info'
    },
    updateStats() {
      this.taskCount = this.allTasks.length
      this.completedTaskCount = this.allTasks.filter(t => t.status === 'completed').length
      this.dataCount = 0 // 实际应该从API获取
      this.recentTasks = [...this.allTasks].sort((a, b) => {
        return new Date(b.created_at) - new Date(a.created_at)
      }).slice(0, 5)
    }
  },
  async created() {
    await this.fetchTasks()
    this.updateStats()
  }
}
</script>

<style scoped>
.home {
  padding: 20px 0;
}

.welcome-card {
  margin-bottom: 20px;
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

.card-content {
  text-align: center;
  padding: 20px 0;
}

.quick-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-top: 10px;
}

.recent-tasks {
  margin-bottom: 20px;
}
</style> 