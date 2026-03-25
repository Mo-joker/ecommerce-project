<template>
  <div class="orders-page">
    <div class="container">
      <h1>我的订单</h1>

      <el-empty v-if="orders.length === 0" description="暂无订单" />

      <div v-else class="order-list">
        <el-card v-for="order in orders" :key="order.id" class="order-card">
          <template #header>
            <div class="order-header">
              <span>订单号: {{ order.order_number }}</span>
              <el-tag :type="getStatusType(order.status)">
                {{ getStatusText(order.status) }}
              </el-tag>
            </div>
          </template>

          <div class="order-items">
            <div v-for="item in order.items" :key="item.product_id" class="order-item">
              <img :src="item.image || 'https://picsum.photos/60/60'" class="item-image">
              <div class="item-info">
                <div class="item-name">{{ item.product_name }}</div>
                <div class="item-price">¥{{ item.price }} x {{ item.quantity }}</div>
              </div>
              <div class="item-total">¥{{ item.total_price }}</div>
            </div>
          </div>

          <div class="order-footer">
            <div class="total">总计: ¥{{ order.total_amount }}</div>
            <el-button type="primary" size="small" @click="viewOrder(order.id)">
              查看详情
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const orders = ref([])

// 临时订单数据（实际应该从 API 获取）
const mockOrders = [
  {
    id: 1,
    order_number: 'ORD20240101123456',
    total_amount: 3999.00,
    status: 'pending',
    items: [
      {
        product_id: 1,
        product_name: '智能手机',
        price: 3999.00,
        quantity: 1,
        total_price: 3999.00,
        image: 'https://picsum.photos/60/60?random=1'
      }
    ],
    created_at: '2024-01-01 12:34:56'
  },
  {
    id: 2,
    order_number: 'ORD20240102123456',
    total_amount: 299.00,
    status: 'paid',
    items: [
      {
        product_id: 4,
        product_name: '纯棉T恤',
        price: 99.00,
        quantity: 2,
        total_price: 198.00,
        image: 'https://picsum.photos/60/60?random=4'
      },
      {
        product_id: 5,
        product_name: '牛仔裤',
        price: 199.00,
        quantity: 1,
        total_price: 199.00,
        image: 'https://picsum.photos/60/60?random=5'
      }
    ],
    created_at: '2024-01-02 12:34:56'
  }
]

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

onMounted(() => {
  // 实际应该从 API 获取
  orders.value = mockOrders
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
}

.item-price {
  color: #666;
  font-size: 12px;
}

.item-total {
  font-weight: bold;
  color: #ff4444;
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
  font-size: 18px;
  font-weight: bold;
}

.total span {
  color: #ff4444;
  font-size: 20px;
}
</style>