<template>
  <div class="profile-page">
    <div class="container">
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span>个人资料</span>
          </div>
        </template>

        <div v-loading="loading" class="profile-content">
          <div class="avatar-section">
            <el-avatar :size="100" :src="userForm.avatar || defaultAvatar">
              <img src="@/assets/proicon.png" alt="avatar">
            </el-avatar>
            <el-button type="primary" size="small" style="margin-left: 20px" @click="showEditAvatar = true">
              更换头像
            </el-button>
          </div>

          <el-form :model="userForm" label-width="100px" style="max-width: 500px; margin: 30px auto">
            <el-form-item label="用户名">
              <el-input v-model="userForm.username" disabled />
            </el-form-item>

            <el-form-item label="邮箱">
              <el-input v-model="userForm.email" disabled />
            </el-form-item>

            <el-form-item label="全名">
              <el-input v-model="userForm.full_name" placeholder="请输入全名" />
            </el-form-item>

            <el-form-item label="角色">
              <el-tag :type="userForm.is_admin ? 'success' : 'info'">
                {{ userForm.is_admin ? '管理员' : '普通用户' }}
              </el-tag>
            </el-form-item>

            <el-form-item label="账号状态">
              <el-tag :type="userForm.is_active ? 'success' : 'danger'">
                {{ userForm.is_active ? '正常' : '禁用' }}
              </el-tag>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handleUpdateProfile" :loading="updating">
                保存修改
              </el-button>
              <el-button @click="router.back()">返回</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- 更换头像对话框 -->
      <el-dialog v-model="showEditAvatar" title="更换头像" width="400px">
        <el-input v-model="userForm.avatar" placeholder="请输入头像 URL" />
        <template #footer>
          <el-button @click="showEditAvatar = false">取消</el-button>
          <el-button type="primary" @click="handleSaveAvatar">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import proiconImage from '@/assets/proicon.png'
import request from '@/api/index'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(true)
const updating = ref(false)
const showEditAvatar = ref(false)
const defaultAvatar = proiconImage

const userForm = reactive({
  username: '',
  email: '',
  full_name: '',
  avatar: '',
  is_admin: false,
  is_active: false
})

// 加载用户信息
const loadUserProfile = async () => {
  loading.value = true
  try {
    await userStore.getUserInfo()
    const userInfo = userStore.userInfo

    if (userInfo) {
      userForm.username = userInfo.username
      userForm.email = userInfo.email
      userForm.full_name = userInfo.full_name || ''
      userForm.avatar = userInfo.avatar || ''
      userForm.is_admin = userInfo.is_admin || false
      userForm.is_active = userInfo.is_active !== undefined ? userInfo.is_active : true
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  } finally {
    loading.value = false
  }
}

// 更新用户资料
const handleUpdateProfile = async () => {
  updating.value = true
  try {
    const res = await request.put('/users/me', {
      full_name: userForm.full_name,
      avatar: userForm.avatar
    })

    // 更新 store 中的用户信息
    await userStore.getUserInfo()

    ElMessage.success('资料更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  } finally {
    updating.value = false
  }
}

// 保存头像
const handleSaveAvatar = async () => {
  try {
    await handleUpdateProfile()
    showEditAvatar.value = false
  } catch (error) {
    console.error('保存头像失败:', error)
  }
}

onMounted(() => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  loadUserProfile()
})
</script>

<style scoped>
.profile-page {
  min-height: calc(100vh - 120px);
  background-color: #f5f5f5;
  padding: 40px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.profile-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-content {
  padding: 20px;
}

.avatar-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-tag) {
  font-size: 14px;
}
</style>
