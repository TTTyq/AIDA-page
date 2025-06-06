import { createRouter, createWebHistory } from 'vue-router'

// 导入视图组件
const Home = () => import('@/views/Home.vue')
const NewTask = () => import('@/views/NewTask.vue')
const TaskList = () => import('@/views/TaskList.vue')
const TaskDetail = () => import('@/views/TaskDetail.vue')
const DataPreview = () => import('@/views/DataPreview.vue')

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/tasks/new',
    name: 'NewTask',
    component: NewTask
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: TaskList
  },
  {
    path: '/tasks/:id',
    name: 'TaskDetail',
    component: TaskDetail,
    props: true
  },
  {
    path: '/data/:taskId',
    name: 'DataPreview',
    component: DataPreview,
    props: true
  }
]

// 创建路由
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 