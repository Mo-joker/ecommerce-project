// src/api/index.js
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
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
    // 直接返回数据
    return response.data
  },
  error => {
    // 处理错误响应
    if (error.response) {
      const { status, data } = error.response

      // 401 未授权
      if (status === 401) {
        ElMessage.error('请重新登录')
        localStorage.removeItem('token')
        // 只在需要认证的页面才跳转
        if (router.currentRoute.value.path !== '/login') {
          router.push('/login')
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
      ElMessage.error('网络连接失败，请检查网络')
    }
    // 其他错误
    else {
      ElMessage.error(error.message || '请求失败')
    }

    return Promise.reject(error)
  }
)

export default request