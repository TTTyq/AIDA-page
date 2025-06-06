import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    tasks: [],
    currentTask: null,
    taskData: [],
    loading: false,
    error: null
  },
  
  mutations: {
    SET_TASKS(state, tasks) {
      state.tasks = tasks
    },
    SET_CURRENT_TASK(state, task) {
      state.currentTask = task
    },
    SET_TASK_DATA(state, data) {
      state.taskData = data
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    ADD_TASK(state, task) {
      state.tasks.push(task)
    },
    REMOVE_TASK(state, taskId) {
      state.tasks = state.tasks.filter(task => task.id !== taskId)
    }
  },
  
  actions: {
    // 获取所有任务
    async fetchTasks({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/api/tasks/')
        commit('SET_TASKS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 获取单个任务
    async fetchTask({ commit }, taskId) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/api/tasks/${taskId}`)
        commit('SET_CURRENT_TASK', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 创建新任务
    async createTask({ commit }, taskData) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.post('/api/tasks/', taskData)
        commit('ADD_TASK', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 删除任务
    async deleteTask({ commit }, taskId) {
      commit('SET_LOADING', true)
      try {
        await axios.delete(`/api/tasks/${taskId}`)
        commit('REMOVE_TASK', taskId)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 运行爬虫
    async runScraper({ commit }, config) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.post('/api/scraper/run', config)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 获取任务数据
    async fetchTaskData({ commit }, taskId) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/api/data/?task_id=${taskId}`)
        commit('SET_TASK_DATA', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 导出数据
    async exportData({ commit }, { taskId, format }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/api/data/export/${taskId}?format=${format}`)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 清除错误
    clearError({ commit }) {
      commit('SET_ERROR', null)
    }
  },
  
  getters: {
    allTasks: state => state.tasks,
    taskById: state => id => state.tasks.find(task => task.id === id),
    isLoading: state => state.loading,
    error: state => state.error,
    currentTask: state => state.currentTask,
    taskData: state => state.taskData
  }
}) 