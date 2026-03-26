<template>
  <div class="orders-page">
    <div class="container">
      <h1>我的订单</h1>

      <!-- 状态筛选 -->
      <div class="filter-tabs">
        <el-radio-group v-model="currentStatus" @change="loadOrders">
          <el-radio-button value="">
            全部 <el-tag v-if="stats.total" size="small" style="margin-left: 5px">{{ stats.total }}</el-tag>
          </el-radio-button>
          <el-radio-button label="pending">
            待支付 <el-tag v-if="stats.pending" size="small" type="warning" style="margin-left: 5px">{{ stats.pending }}</el-tag>
          </el-radio-button>
          <el-radio-button label="paid">
            已支付 <el-tag v-if="stats.paid" size="small" type="info" style="margin-left: 5px">{{ stats.paid }}</el-tag>
          </el-radio-button>
          <el-radio-button label="shipped">
            已发货 <el-tag v-if="stats.shipped" size="small" type="primary" style="margin-left: 5px">{{ stats.shipped }}</el-tag>
          </el-radio-button>
          <el-radio-button label="completed">
            已完成 <el-tag v-if="stats.completed" size="small" type="success" style="margin-left: 5px">{{ stats.completed }}</el-tag>
          </el-radio-button>
          <el-radio-button label="cancelled">
            已取消 <el-tag v-if="stats.cancelled" size="small" type="danger" style="margin-left: 5px">{{ stats.cancelled }}</el-tag>
          </el-radio-button>
        </el-radio-group>
      </div>

      <div v-loading="loading" element-loading-text="加载中...">
        <el-empty v-if="!loading && orders.length === 0" description="暂无订单" />

        <div v-else class="order-list">
          <el-card v-for="order in orders" :key="order.id" class="order-card">
            <template #header>
              <div class="order-header">
                <div>
                  <div class="order-number">订单号：{{ order.order_number }}</div>
                  <div class="order-time" style="font-size: 12px; color: #999; margin-top: 5px">
                    下单时间：{{ formatDate(order.created_at) }}
                  </div>
                </div>
                <el-tag :type="getStatusType(order.status)">
                  {{ getStatusText(order.status) }}
                </el-tag>
              </div>
            </template>

            <div class="order-items">
              <div v-for="item in order.items" :key="item.product_id" class="order-item">
                <img :src="proiconImage" class="item-image" alt="商品图片">
                <div class="item-info">
                  <div class="item-name">{{ item.product_name }}</div>
                  <div class="item-price">¥{{ item.price }} x {{ item.quantity }}</div>
                </div>
                <div class="item-total">¥{{ item.total_price }}</div>
              </div>
            </div>

            <div class="order-footer">
              <div class="total">总计：<span>¥{{ order.total_amount }}</span></div>
              <div class="actions">
                <el-button
                  v-if="order.status === 'pending'"
                  type="danger"
                  size="small"
                  @click="cancelOrder(order)"
                >
                  取消订单
                </el-button>
                <el-button
                  v-if="order.status === 'pending'"
                  type="success"
                  size="small"
                  @click="payOrder(order)"
                >
                  立即付款
                </el-button>
                <el-button type="primary" size="small" @click="viewOrder(order.id)">
                  查看详情
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { orderApi } from '@/api/order'
import proiconImage from '@/assets/proicon.png'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(true)
const orders = ref([])
const currentStatus = ref('')
const stats = ref({
  total: 0,
  pending: 0,
  paid: 0,
  shipped: 0,
  completed: 0,
  cancelled: 0
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusType = (status) => {
  const map = {
    pending: 'warning',
    paid: 'info',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    pending: '待支付',
    paid: '已支付',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

const viewOrder = (orderId) => {
  router.push(`/order/${orderId}`)
}

const cancelOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消订单 ${order.order_number} 吗？`,
      '取消订单',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await orderApi.cancelOrder(order.id)

    ElMessage.success('订单已取消')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败')
    }
  }
}

const payOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确认支付订单 ${order.order_number} 吗？`,
      '支付订单',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }
    )

    await orderApi.payOrder(order.id)

    ElMessage.success('支付成功')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('支付失败:', error)
      ElMessage.error('支付失败')
    }
  }
}

// 加载订单统计
const loadStats = async () => {
  try {
    // 获取所有订单
    const allOrders = await orderApi.getOrders({})

    // 统计各状态订单数
    stats.value = {
      total: allOrders.length,
      pending: allOrders.filter(o => o.status === 'pending').length,
      paid: allOrders.filter(o => o.status === 'paid').length,
      shipped: allOrders.filter(o => o.status === 'shipped').length,
      completed: allOrders.filter(o => o.status === 'completed').length,
      cancelled: allOrders.filter(o => o.status === 'cancelled').length
    }
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const loadOrders = async () => {
  loading.value = true
  try {
    const params = {}
    if (currentStatus.value) {
      params.status = currentStatus.value
    }

    console.log('===== 订单筛选 =====')
    console.log('当前筛选状态:', currentStatus.value || '全部')
    console.log('请求参数对象:', params)
    console.log('参数是否为空:', Object.keys(params).length === 0)

    // 调用 API
    const res = await orderApi.getOrders(params)

    console.log('返回订单数:', res.length)
    if (res.length > 0) {
      console.log('订单状态分布:', res.map(o => o.status))
    }

    orders.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('加载订单失败:', error)
    ElMessage.error('加载订单失败')
    orders.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  loadStats()
  loadOrders()
})
</script>

<style scoped>
.orders-page {
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

.filter-tabs {
  margin-bottom: 20px;
  padding: 15px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  border-radius: 8px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-number {
  font-weight: bold;
  color: #333;
}

.order-items {
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 14px;
}

.item-price {
  color: #666;
  font-size: 13px;
}

.item-total {
  font-weight: bold;
  color: #ff4444;
  font-size: 16px;
}

.order-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.total {
  font-size: 16px;
  color: #666;
}

.total span {
  color: #ff4444;
  font-size: 20px;
  font-weight: bold;
  margin-left: 5px;
}
</style>