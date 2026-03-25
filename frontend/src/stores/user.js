import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),

  actions: {
    async login(credentials) {
      try {
        const res = await authApi.login(credentials)
        this.token = res.access_token
        localStorage.setItem('token', this.token)
        await this.getUserInfo()
        ElMessage.success('登录成功')
        return true
      } catch (error) {
        console.error('登录失败', error)
        return false
      }
    },

    async register(userData) {
      try {
        const res = await authApi.register(userData)
        this.token = res.access_token
        localStorage.setItem('token', this.token)
        ElMessage.success('注册成功')
        return true
      } catch (error) {
        console.error('注册失败', error)
        return false
      }
    },

    async getUserInfo() {
      try {
        const res = await authApi.getCurrentUser()
        this.userInfo = res
      } catch (error) {
        console.error('获取用户信息失败', error)
      }
    },

    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
      ElMessage.success('已退出登录')
    }
  },

  getters: {
    isLoggedIn: (state) => !!state.token,
    userName: (state) => state.userInfo?.username || ''
  }
})