<template>
  <div class="order-detail-page">
    <div class="container" v-loading="loading">
      <el-button class="back-btn" @click="router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>

      <div v-if="order">
        <div class="order-header">
          <h1>订单详情</h1>
          <el-tag :type="getStatusType(order.status)" size="large">
            {{ getStatusText(order.status) }}
          </el-tag>
        </div>

        <el-row :gutter="20">
          <!-- 订单信息 -->
          <el-col :span="16">
            <el-card class="info-card">
              <template #header>
                <span>订单信息</span>
              </template>

              <el-descriptions :column="2" border>
                <el-descriptions-item label="订单号">
                  {{ order.order_number }}
                </el-descriptions-item>
                <el-descriptions-item label="下单时间">
                  {{ formatDate(order.created_at) }}
                </el-descriptions-item>
                <el-descriptions-item label="订单状态">
                  <el-tag :type="getStatusType(order.status)">
                    {{ getStatusText(order.status) }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="支付方式">
                  在线支付
                </el-descriptions-item>
              </el-descriptions>
            </el-card>

            <!-- 收货信息 -->
            <el-card class="info-card">
              <template #header>
                <span>收货信息</span>
              </template>

              <el-descriptions :column="1" border>
                <el-descriptions-item label="收货人">
                  {{ order.address?.name || '张三' }}
                </el-descriptions-item>
                <el-descriptions-item label="联系电话">
                  {{ order.phone || '138****0000' }}
                </el-descriptions-item>
                <el-descriptions-item label="收货地址">
                  {{ order.address?.detail || '北京市朝阳区xxx街道xxx号' }}
                </el-descriptions-item>
              </el-descriptions>
            </el-card>

            <!-- 商品列表 -->
            <el-card class="info-card">
              <template #header>
                <span>商品列表</span>
              </template>

              <el-table :data="order.items" style="width: 100%">
                <el-table-column label="商品">
                  <template #default="{ row }">
                    <div class="product-cell">
                      <img :src="row.image || 'https://picsum.photos/60/60'" class="product-image">
                      <div class="product-info">
                        <div class="product-name">{{ row.product_name }}</div>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="单价" width="120">
                  <template #default="{ row }">
                    ¥{{ row.price }}
                  </template>
                </el-table-column>
                <el-table-column label="数量" width="100">
                  <template #default="{ row }">
                    x{{ row.quantity }}
                  </template>
                </el-table-column>
                <el-table-column label="小计" width="120">
                  <template #default="{ row }">
                    <span class="price">¥{{ row.total_price || (row.price * row.quantity).toFixed(2) }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>

          <!-- 订单汇总 -->
          <el-col :span="8">
            <el-card class="summary-card">
              <template #header>
                <span>订单汇总</span>
              </template>

              <div class="summary-item">
                <span>商品总额</span>
                <span>¥{{ order.total_amount }}</span>
              </div>
              <div class="summary-item">
                <span>运费</span>
                <span>¥0.00</span>
              </div>
              <div class="summary-item total">
                <span>实付金额</span>
                <span class="total-price">¥{{ order.total_amount }}</span>
              </div>

              <div class="order-actions" v-if="order.status === 'pending'">
                <el-button type="primary" size="large" block @click="handlePay">
                  立即支付
                </el-button>
                <el-button size="large" block @click="handleCancel">
                  取消订单
                </el-button>
              </div>

              <div class="order-actions" v-if="order.status === 'paid'">
                <el-button type="primary" size="large" block @click="handleTrack">
                  查看物流
                </el-button>
              </div>

              <div class="order-actions" v-if="order.status === 'completed'">
                <el-button type="success" size="large" block @click="handleReview">
                  评价商品
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <el-empty v-else description="订单不存在" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { orderApi } from '@/api/order'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const order = ref(null)

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

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const loadOrderDetail = async () => {
  const orderId = parseInt(route.params.id)
  if (!orderId) return

  loading.value = true
  try {
    // 调用真实 API
    const data = await orderApi.getOrder(orderId)
    console.log('订单详情:', data)
    order.value = data
  } catch (error) {
    console.error('加载订单详情失败:', error)

    let errorMsg = '加载失败'
    if (error.response?.status === 404) {
      errorMsg = '订单不存在或您无权查看'
    } else if (error.response?.status === 401) {
      errorMsg = '请先登录'
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    }

    ElMessage.error(errorMsg)

    // 延迟返回订单列表页
    setTimeout(() => {
      router.push('/orders')
    }, 2000)
  } finally {
    loading.value = false
  }
}

const handlePay = async () => {
  try {
    await ElMessageBox.confirm('确认支付该订单吗？', '提示', {
      confirmButtonText: '确认支付',
      cancelButtonText: '取消',
      type: 'info'
    })

    await orderApi.payOrder(order.value.id)

    ElMessage.success('支付成功')
    order.value.status = 'paid'
  } catch (error) {
    if (error !== 'cancel') {
      console.error('支付失败:', error)
      ElMessage.error('支付失败')
    }
  }
}

const handleCancel = async () => {
  try {
    await ElMessageBox.confirm('确认取消该订单吗？', '提示', {
      confirmButtonText: '确认取消',
      cancelButtonText: '返回',
      type: 'warning'
    })

    await orderApi.cancelOrder(order.value.id)

    ElMessage.success('订单已取消')
    order.value.status = 'cancelled'
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消失败:', error)
      ElMessage.error('取消失败')
    }
  }
}

const handleTrack = () => {
  ElMessage.info('物流信息：您的商品正在配送中...')
}

const handleReview = () => {
  ElMessage.info('评价功能开发中...')
}

onMounted(() => {
  loadOrderDetail()
})
</script>

<style scoped>
.order-detail-page {
  min-height: calc(100vh - 120px);
  background-color: #f5f5f5;
  padding: 20px 0 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-btn {
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.order-header h1 {
  margin: 0;
  font-size: 24px;
}

.info-card,
.summary-card {
  margin-bottom: 20px;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 15px;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.product-name {
  font-weight: 500;
}

.price {
  color: #ff4444;
  font-weight: bold;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.summary-item.total {
  border-top: 1px solid #eee;
  border-bottom: none;
  margin-top: 10px;
  padding-top: 15px;
  font-size: 18px;
  font-weight: bold;
}

.total-price {
  color: #ff4444;
  font-size: 20px;
}

.order-actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>