<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-brand">
        <router-link to="/">商城</router-link>
      </div>

      <div class="nav-menu">
        <router-link to="/">首页</router-link>
        <router-link to="/products">商品</router-link>
        <router-link to="/orders" v-if="userStore.isLoggedIn">我的订单</router-link>
      </div>

      <div class="nav-actions">
        <router-link to="/cart" class="cart-link">
          <el-icon><ShoppingCart /></el-icon>
          <span class="cart-badge" v-if="cartStore.totalItems > 0">
            {{ cartStore.totalItems }}
          </span>
        </router-link>

        <div v-if="userStore.isLoggedIn" class="user-menu">
          <el-dropdown @command="handleCommand">
            <span class="user-name">
              {{ userStore.userName }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="orders">我的订单</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>

        <div v-else class="auth-links">
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'
import { ShoppingCart, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/')
  } else if (command === 'orders') {
    router.push('/orders')
  }
}
</script>

<style scoped>
.navbar {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.nav-brand a {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-menu a {
  color: #333;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-menu a:hover {
  color: #409eff;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.cart-link {
  position: relative;
  color: #333;
  text-decoration: none;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -12px;
  background-color: #ff4444;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
  min-width: 18px;
  text-align: center;
}

.user-name {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.auth-links {
  display: flex;
  gap: 15px;
}

.auth-links a {
  color: #333;
  text-decoration: none;
}

.auth-links a:hover {
  color: #409eff;
}
</style>