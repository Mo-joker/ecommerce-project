<template>
  <div class="product-detail-page">
    <div class="container" v-loading="loading">
      <el-row :gutter="30" v-if="product">
        <el-col :span="12">
          <div class="product-images">
            <el-image
              :src="product.images?.[0] || 'https://picsum.photos/500/500'"
              fit="cover"
              class="main-image"
            />
          </div>
        </el-col>

        <el-col :span="12">
          <div class="product-info">
            <h1>{{ product.name }}</h1>
            <p class="description">{{ product.description }}</p>
            <div class="price">¥{{ product.price }}</div>
            <div class="stock">库存：{{ product.stock }} 件</div>

            <div class="quantity">
              <span>数量:</span>
              <el-input-number
                v-model="quantity"
                :min="1"
                :max="product.stock"
                size="large"
              />
            </div>

            <div class="actions">
              <el-button
                type="primary"
                size="large"
                :disabled="product.stock === 0 || addingToCart"
                :loading="addingToCart"
                @click="addToCart"
              >
                加入购物车
              </el-button>
              <el-button
                type="success"
                size="large"
                :disabled="product.stock === 0 || addingToCart"
                :loading="addingToCart"
                @click="buyNow"
              >
                立即购买
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { productApi } from '@/api/product'
import { useCartStore } from '@/stores/cart'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const loading = ref(false)
const product = ref(null)
const quantity = ref(1)
const addingToCart = ref(false)

const loadProduct = async () => {
  const id = route.params.id
  if (!id) return

  loading.value = true
  try {
    const res = await productApi.getProduct(id)
    product.value = res
  } catch (error) {
    console.error('加载商品失败', error)
    ElMessage.error('商品不存在')
    router.push('/products')
  } finally {
    loading.value = false
  }
}

const checkAuth = () => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning({
      message: '请先登录后再操作',
      duration: 1500
    })
    setTimeout(() => {
      router.push('/login')
    }, 1500)
    return false
  }
  return true
}

const addToCart = async () => {
  if (!product.value || addingToCart.value) return
  if (!checkAuth()) return

  addingToCart.value = true
  try {
    await cartStore.addItem(product.value, quantity.value)
  } finally {
    addingToCart.value = false
  }
}

const buyNow = async () => {
  if (!checkAuth()) return

  addingToCart.value = true
  try {
    await cartStore.addItem(product.value, quantity.value)
    setTimeout(() => {
      router.push('/cart')
    }, 1000)
  } catch (error) {
    console.error('添加失败:', error)
    addingToCart.value = false
  }
}

onMounted(() => {
  loadProduct()
})
</script>

<style scoped>
.product-detail-page {
  min-height: calc(100vh - 120px);
  background-color: #f5f5f5;
  padding: 40px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.product-images {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.main-image {
  width: 100%;
  height: 400px;
  border-radius: 8px;
}

.product-info {
  background: white;
  border-radius: 8px;
  padding: 30px;
}

.product-info h1 {
  font-size: 24px;
  margin-bottom: 15px;
}

.description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.price {
  font-size: 28px;
  color: #ff4444;
  font-weight: bold;
  margin-bottom: 15px;
}

.stock {
  color: #666;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.quantity {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  gap: 15px;
}
</style>