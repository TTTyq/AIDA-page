<template>
  <div class="new-task">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>创建新爬虫任务</h2>
        </div>
      </template>
      
      <el-form :model="taskForm" :rules="rules" ref="taskForm" label-width="120px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        
        <el-form-item label="目标URL" prop="url">
          <el-input v-model="taskForm.url" placeholder="请输入目标URL"></el-input>
        </el-form-item>
        
        <el-form-item label="任务描述">
          <el-input v-model="taskForm.description" type="textarea" rows="3" placeholder="请输入任务描述"></el-input>
        </el-form-item>
        
        <el-divider>爬虫配置</el-divider>
        
        <el-form-item label="CSS选择器" prop="selector">
          <el-input v-model="taskForm.config.selector" placeholder="例如: div.content, .article, #main"></el-input>
          <div class="form-tip">用于选择要爬取的元素，如果不确定，可以使用浏览器开发者工具查看</div>
        </el-form-item>
        
        <el-form-item label="使用浏览器">
          <el-switch v-model="taskForm.config.use_browser"></el-switch>
          <div class="form-tip">对于需要JavaScript渲染的页面，请启用此选项</div>
        </el-form-item>
        
        <el-form-item label="等待时间(秒)" v-if="taskForm.config.use_browser">
          <el-input-number v-model="taskForm.config.wait_time" :min="0" :max="30"></el-input-number>
          <div class="form-tip">等待页面加载完成的时间，对于复杂页面可能需要增加</div>
        </el-form-item>
        
        <el-form-item label="启用分页">
          <el-switch v-model="taskForm.config.pagination"></el-switch>
          <div class="form-tip">如果需要爬取多页内容，请启用此选项</div>
        </el-form-item>
        
        <el-form-item label="最大页数" v-if="taskForm.config.pagination">
          <el-input-number v-model="taskForm.config.max_pages" :min="1" :max="100"></el-input-number>
          <div class="form-tip">限制爬取的最大页数，避免无限爬取</div>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">创建任务</el-button>
          <el-button @click="testUrl" :loading="testing">测试URL</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import axios from 'axios'

export default {
  name: 'NewTask',
  data() {
    return {
      taskForm: {
        name: '',
        url: '',
        description: '',
        config: {
          selector: 'body',
          use_browser: false,
          wait_time: 0,
          pagination: false,
          max_pages: 1
        }
      },
      rules: {
        name: [
          { required: true, message: '请输入任务名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        url: [
          { required: true, message: '请输入目标URL', trigger: 'blur' },
          { pattern: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/, message: '请输入有效的URL', trigger: 'blur' }
        ],
        selector: [
          { required: true, message: '请输入CSS选择器', trigger: 'blur' }
        ]
      },
      testing: false
    }
  },
  computed: {
    ...mapGetters(['isLoading', 'error']),
    loading() {
      return this.isLoading
    }
  },
  methods: {
    ...mapActions(['createTask', 'clearError']),
    async submitForm() {
      try {
        await this.$refs.taskForm.validate()
        
        // 创建任务
        const task = await this.createTask({
          name: this.taskForm.name,
          description: this.taskForm.description,
          url: this.taskForm.url,
          config: this.taskForm.config
        })
        
        this.$message.success('任务创建成功')
        this.$router.push(`/tasks/${task.id}`)
      } catch (error) {
        if (error) {
          this.$message.error('表单验证失败，请检查输入')
        }
      }
    },
    resetForm() {
      this.$refs.taskForm.resetFields()
    },
    async testUrl() {
      if (!this.taskForm.url) {
        this.$message.warning('请先输入URL')
        return
      }
      
      this.testing = true
      try {
        const response = await axios.get(`/api/scraper/test/${encodeURIComponent(this.taskForm.url)}`)
        if (response.data.status === 'ok') {
          this.$message.success('URL可访问')
        } else {
          this.$message.warning('URL可能无法访问')
        }
      } catch (error) {
        this.$message.error('URL测试失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.testing = false
      }
    }
  },
  created() {
    this.clearError()
  }
}
</script>

<style scoped>
.new-task {
  max-width: 800px;
  margin: 0 auto;
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

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style> 