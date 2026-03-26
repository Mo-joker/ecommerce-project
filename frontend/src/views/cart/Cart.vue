<template>
  <div class="cart-page">
    <div class="container">
      <h1>我的购物车</h1>

      <div v-loading="loading" element-loading-text="加载中...">
        <el-empty v-if="!loading && cartItems.length === 0" description="购物车是空的" />

        <div v-else class="cart-list">
          <el-card class="cart-header">
            <div class="header-row">
              <span class="col-product">商品信息</span>
              <span class="col-price">单价</span>
              <span class="col-quantity">数量</span>
              <span class="col-total">小计</span>
              <span class="col-action">操作</span>
            </div>
          </el-card>

          <el-card v-for="item in cartItems" :key="item.id" class="cart-item">
            <div class="item-row">
              <div class="col-product">
                <img :src="item.product_image || proiconImage" class="product-image" alt="商品图片">
                <span class="product-name">{{ item.product_name }}</span>
              </div>
              <div class="col-price">¥{{ item.product_price }}</div>
              <div class="col-quantity">
                <el-input-number
                  v-model="item.quantity"
                  :min="1"
                  :max="99"
                  size="small"
                  @change="updateQuantity(item)"
                />
              </div>
              <div class="col-total">¥{{ (item.product_price * item.quantity).toFixed(2) }}</div>
              <div class="col-action">
                <el-button type="danger" size="small" @click="removeItem(item)">删除</el-button>
              </div>
            </div>
          </el-card>

          <el-card v-if="cartItems.length > 0" class="cart-summary">
            <div class="summary-row">
              <div class="total-info">
                <span>共 {{ totalItems }} 件商品</span>
                <span style="margin-left: 20px">总计：<span class="total-price">¥{{ totalPrice.toFixed(2) }}</span></span>
              </div>
              <div class="actions">
                <el-button @click="clearCart">清空购物车</el-button>
                <el-button
                  type="primary"
                  @click="checkout"
                  :loading="checkoutLoading"
                >
                  去结算
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { orderApi } from '@/api/order'
import proiconImage from '@/assets/proicon.png'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()
const loading = ref(true)
const checkoutLoading = ref(false)

const cartItems = computed(() => cartStore.items)
const totalItems = computed(() => cartStore.totalItems)
const totalPrice = computed(() => cartStore.totalPrice)

const updateQuantity = async (item) => {
  await cartStore.updateQuantity(item.id, item.quantity)
}

const removeItem = async (item) => {
  await cartStore.removeItem(item.id)
}

const clearCart = async () => {
  await cartStore.clearCart()
}

const checkout = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  if (cartItems.value.length === 0) {
    ElMessage.warning('购物车是空的')
    return
  }

  // 防止重复点击
  if (checkoutLoading.value) {
    return
  }

  checkoutLoading.value = true

  try {
    console.log('准备创建订单，商品数据:', cartItems.value)

    // 准备订单数据
    const orderData = {
      items: cartItems.value.map(item => ({
        product_id: item.product_id,
        price: item.product_price,
        quantity: item.quantity
      })),
      total_amount: totalPrice.value,
      address: '默认地址',
      phone: '1234567890'
    }

    console.log('发送订单数据:', orderData)

    // 检查 token
    const token = localStorage.getItem('token')
    console.log('当前 token:', token ? '存在' : '不存在')

    // 创建订单
    const order = await orderApi.createOrder(orderData)

    console.log('订单创建成功:', order)

    // 清空购物车（不显示提示，避免重复）
    await cartStore.clearCartWithoutMessage()

    ElMessage.success({
      message: '订单创建成功',
      duration: 1500
    })

    // 跳转到订单详情页
    setTimeout(() => {
      router.push(`/order/${order.id}`)
    }, 500)
  } catch (error) {
    console.error('创建订单失败 - 完整错误:', error)
    console.error('错误响应:', error.response)
    console.error('错误消息:', error.message)
    console.error('错误堆栈:', error.stack)

    // 更详细的错误信息
    let errorMsg = '创建订单失败'
    if (error.response?.status === 401) {
      errorMsg = '登录已过期，请重新登录'
      localStorage.removeItem('token')
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else if (error.response?.data?.detail) {
      errorMsg = error.response.data.detail
    } else if (error.message) {
      errorMsg = error.message
    }

    ElMessage.error(errorMsg)
  } finally {
    checkoutLoading.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    if (userStore.isLoggedIn) {
      await cartStore.loadCart()
    }
  } catch (error) {
    console.error('加载购物车失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cart-page {
  min-height: calc(100vh - 120px);
  background-color: #f5f5f5;
  padding: 40px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

h1 {
  margin-bottom: 30px;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.cart-header {
  border-radius: 8px;
}

.header-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 20px;
  font-weight: bold;
  color: #333;
  padding: 10px 0;
}

.cart-item {
  border-radius: 8px;
}

.item-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 20px;
  align-items: center;
  padding: 15px 0;
}

.col-product {
  display: flex;
  align-items: center;
  gap: 15px;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.product-name {
  font-weight: bold;
  flex: 1;
}

.col-price, .col-total {
  text-align: center;
  font-weight: bold;
  color: #ff4444;
}

.col-quantity {
  display: flex;
  justify-content: center;
}

.col-action {
  text-align: center;
}

.cart-summary {
  border-radius: 8px;
  margin-top: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}

.total-info {
  font-size: 16px;
}

.total-price {
  font-size: 24px;
  font-weight: bold;
  color: #ff4444;
}

.actions {
  display: flex;
  gap: 15px;
}
</style>