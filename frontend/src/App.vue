<template>
  <div id="app">
    <NavBar v-if="showNavBar" />
    <router-view />
    <Footer v-if="showFooter" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'

const route = useRoute()

// 登录和注册页面不显示导航栏和页脚
const showNavBar = computed(() => {
  return route.path !== '/login' && route.path !== '/register'
})

const showFooter = computed(() => {
  return route.path !== '/login' && route.path !== '/register'
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
</style>