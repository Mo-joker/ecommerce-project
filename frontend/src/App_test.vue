<template>
  <div>
    <h1>测试页面</h1>
    <p>如果能看到这个页面，说明 Vue 运行正常</p>
    <button @click="testApi">测试API</button>
    <pre>{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const result = ref('')

const testApi = async () => {
  try {
    const res = await axios.get('/api/v1/products', { params: { limit: 5 } })
    result.value = JSON.stringify(res.data, null, 2)
  } catch (error) {
    result.value = '错误: ' + error.message
  }
}
</script>