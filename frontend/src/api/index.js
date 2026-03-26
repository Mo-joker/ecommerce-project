// src/api/index.js
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

const request = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  // 简单请求不需要预检
  withCredentials: false
})

// 请求拦截器 - 简化 headers
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // 确保 Content-Type 是简单请求允许的
    if (!config.headers['Content-Type']) {
      config.headers['Content-Type'] = 'application/json'
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      const { status, data } = error.response

      // 401 未授权
      if (status === 401) {
        const token = localStorage.getItem('token')
        if (token) {
          ElMessage.error('登录已过期，请重新登录')
          localStorage.removeItem('token')
          setTimeout(() => {
            router.push('/login')
          }, 1500)
        }
      }
      // 403 禁止访问
      else if (status === 403) {
        ElMessage.error(data?.detail || '没有权限访问')
      }
      // 404 未找到
      else if (status === 404) {
        ElMessage.error(data?.detail || '请求的资源不存在')
      }
      // 500 服务器错误
      else if (status >= 500) {
        ElMessage.error('服务器错误，请稍后重试')
      }
      // 其他错误
      else {
        ElMessage.error(data?.detail || data?.message || '请求失败')
      }
    }
    // 网络错误
    else if (error.request) {
      console.error('网络错误:', error)
      ElMessage.error('网络连接失败，请检查后端服务是否启动')
    }
    // 其他错误
    else {
      ElMessage.error(error.message || '请求失败')
    }

    return Promise.reject(error)
  }
)

export default request