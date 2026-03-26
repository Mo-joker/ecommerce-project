import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null,
    fetchingUserInfo: false // 添加标记防止重复请求
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
      // 防止重复请求
      if (this.fetchingUserInfo || !this.token || this.userInfo) {
        return
      }

      this.fetchingUserInfo = true
      try {
        const res = await authApi.getCurrentUser()
        this.userInfo = res
      } catch (error) {
        console.error('获取用户信息失败', error)
      } finally {
        this.fetchingUserInfo = false
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
    userName: (state) => state.userInfo?.username || '',
    isAdmin: (state) => state.userInfo?.is_admin || false
  }
})