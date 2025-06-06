<template>
  <div class="app-header">
    <div class="logo">
      <h1>AIDA 爬虫工具</h1>
    </div>
    <div class="actions">
      <el-button type="primary" @click="$router.push('/tasks/new')">新建任务</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppHeader'
}
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
}

.logo h1 {
  margin: 0;
  font-size: 20px;
  color: #409EFF;
}

.actions {
  display: flex;
  gap: 10px;
}
</style> 