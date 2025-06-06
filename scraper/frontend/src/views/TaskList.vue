<template>
  <div class="task-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>爬虫任务列表</h2>
          <el-button type="primary" @click="$router.push('/tasks/new')">新建任务</el-button>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="tasks"
        style="width: 100%"
        empty-text="暂无任务数据"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="url" label="URL" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewTask(scope.row.id)">查看</el-button>
            <el-button 
              size="small" 
              type="success" 
              :disabled="scope.row.status === 'running'"
              @click="runTask(scope.row)"
            >
              运行
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="confirmDelete(scope.row.id)"
            >
              删除
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
  name: 'TaskList',
  computed: {
    ...mapGetters(['allTasks', 'isLoading']),
    tasks() {
      return this.allTasks
    },
    loading() {
      return this.isLoading
    }
  },
  methods: {
    ...mapActions(['fetchTasks', 'deleteTask', 'runScraper']),
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
    viewTask(id) {
      this.$router.push(`/tasks/${id}`)
    },
    async runTask(task) {
      try {
        await this.runScraper(task.config)
        this.$message.success('任务运行成功')
        this.fetchTasks() // 刷新任务列表
      } catch (error) {
        this.$message.error('任务运行失败: ' + error.message)
      }
    },
    confirmDelete(id) {
      this.$confirm('确认删除此任务？此操作不可恢复', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await this.deleteTask(id)
        this.$message.success('删除成功')
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    }
  },
  created() {
    this.fetchTasks()
  }
}
</script>

<style scoped>
.task-list {
  padding: 20px 0;
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
</style> 