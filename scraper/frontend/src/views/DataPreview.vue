<template>
  <div class="data-preview" v-loading="loading">
    <el-page-header @back="goBack" :title="'返回任务详情'" content="数据预览" />
    
    <el-card class="mt-20">
      <template #header>
        <div class="card-header">
          <h2>爬取数据 ({{ dataItems.length }} 条)</h2>
          <div>
            <el-button @click="exportData('json')">导出JSON</el-button>
            <el-button @click="refreshData">刷新数据</el-button>
          </div>
        </div>
      </template>
      
      <template v-if="dataItems.length > 0">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="表格视图" name="table">
            <el-table :data="dataItems" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="content.title" label="标题" show-overflow-tooltip />
              <el-table-column label="链接数" width="100">
                <template #default="scope">
                  {{ scope.row.content.links ? scope.row.content.links.length : 0 }}
                </template>
              </el-table-column>
              <el-table-column label="图片数" width="100">
                <template #default="scope">
                  {{ scope.row.content.images ? scope.row.content.images.length : 0 }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button 
                    size="small" 
                    @click="showDetail(scope.row)"
                  >
                    查看详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="JSON视图" name="json">
            <div class="json-view">
              <pre>{{ JSON.stringify(dataItems, null, 2) }}</pre>
            </div>
          </el-tab-pane>
        </el-tabs>
      </template>
      
      <el-empty v-else description="暂无数据" />
    </el-card>
    
    <!-- 数据详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="数据详情"
      width="70%"
    >
      <template v-if="currentItem">
        <el-tabs>
          <el-tab-pane label="文本内容">
            <div class="content-text">
              {{ currentItem.content.text }}
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="链接">
            <el-table :data="currentItem.content.links || []" style="width: 100%">
              <el-table-column prop="index" label="#" width="50">
                <template #default="scope">
                  {{ scope.$index + 1 }}
                </template>
              </el-table-column>
              <el-table-column prop="link" label="链接">
                <template #default="scope">
                  <a :href="scope.row" target="_blank">{{ scope.row }}</a>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="图片">
            <div v-if="currentItem.content.images && currentItem.content.images.length > 0" class="image-grid">
              <div v-for="(img, index) in currentItem.content.images" :key="index" class="image-item">
                <img :src="img" :alt="`图片 ${index + 1}`" />
                <div class="image-url">{{ img }}</div>
              </div>
            </div>
            <el-empty v-else description="无图片" />
          </el-tab-pane>
          
          <el-tab-pane label="HTML">
            <div class="html-content">
              <pre>{{ currentItem.content.html }}</pre>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="JSON">
            <div class="json-view">
              <pre>{{ JSON.stringify(currentItem.content, null, 2) }}</pre>
            </div>
          </el-tab-pane>
        </el-tabs>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'DataPreview',
  props: {
    taskId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      activeTab: 'table',
      dialogVisible: false,
      currentItem: null
    }
  },
  computed: {
    ...mapGetters(['isLoading', 'taskData']),
    loading() {
      return this.isLoading
    },
    dataItems() {
      return this.taskData
    }
  },
  methods: {
    ...mapActions(['fetchTaskData', 'exportData']),
    goBack() {
      this.$router.push(`/tasks/${this.taskId}`)
    },
    showDetail(item) {
      this.currentItem = item
      this.dialogVisible = true
    },
    async refreshData() {
      await this.fetchTaskData(this.taskId)
      this.$message.success('数据已刷新')
    },
    async exportDataFile(format) {
      try {
        await this.exportData({
          taskId: this.taskId,
          format
        })
        this.$message.success(`数据已导出为${format.toUpperCase()}格式`)
      } catch (error) {
        this.$message.error('导出失败: ' + error.message)
      }
    }
  },
  created() {
    this.fetchTaskData(this.taskId)
  }
}
</script>

<style scoped>
.data-preview {
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

.json-view {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 10px;
  overflow: auto;
  max-height: 500px;
}

.json-view pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.content-text {
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 400px;
  overflow: auto;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.html-content {
  max-height: 400px;
  overflow: auto;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.html-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.image-item {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-url {
  padding: 5px;
  font-size: 12px;
  color: #606266;
  word-break: break-all;
  background-color: #f5f5f5;
}
</style> 