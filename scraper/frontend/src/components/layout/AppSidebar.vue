<template>
  <div class="sidebar">
    <el-menu
      :default-active="activeIndex"
      router
      class="sidebar-menu"
    >
      <el-menu-item index="/">
        <el-icon><i class="el-icon-house"></i></el-icon>
        <span>Home</span>
      </el-menu-item>
      <el-menu-item index="/websites">
        <el-icon><i class="el-icon-monitor"></i></el-icon>
        <span>Websites</span>
      </el-menu-item>
      <el-menu-item index="/tasks">
        <el-icon><i class="el-icon-list"></i></el-icon>
        <span>Tasks</span>
      </el-menu-item>
      <el-menu-item index="/tasks/new">
        <el-icon><i class="el-icon-plus"></i></el-icon>
        <span>New Task</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'AppSidebar',
  computed: {
    activeIndex() {
      return this.$route.path
    }
  }
}
</script>

<style scoped>
.sidebar {
  height: 100%;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}
</style> 