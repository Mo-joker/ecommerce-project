<template>
  <el-card class="product-card" :body-style="{ padding: '0px' }">
    <div class="product-image">
      <img :src="getImageUrl" :alt="product.name">
    </div>
    <div class="product-info">
      <h3>{{ product.name }}</h3>
      <p class="description">{{ product.description }}</p>
      <div class="price">¥{{ product.price }}</div>
      <div class="actions">
        <el-button type="primary" size="small" @click="viewDetail">查看详情</el-button>
        <el-button type="success" size="small" @click="addToCart">加入购物车</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ElMessage } from 'element-plus'
import proiconImage from '@/assets/proicon.png'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const cartStore = useCartStore()

// 使用固定的本地图片
const getImageUrl = computed(() => {
  // 如果商品有自定义图片，优先使用
  if (props.product.images?.[0]) {
    return props.product.images[0]
  }

  // 默认使用 proicon.png
  return proiconImage
})

const viewDetail = () => {
  router.push(`/product/${props.product.id}`)
}

const addToCart = () => {
  cartStore.addItem(props.product)
  ElMessage.success('已加入购物车')
}
</script>

<style scoped>
.product-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  height: 200px;
  overflow: hidden;
  background-color: #f0f0f0;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 15px;
}

.product-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
}

.description {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price {
  color: #ff4444;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  gap: 10px;
}
</style>