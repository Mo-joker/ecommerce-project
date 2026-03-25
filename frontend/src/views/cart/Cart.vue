<template>
  <div class="cart-page">
    <div class="container">
      <h1>购物车</h1>

      <el-empty v-if="cartStore.items.length === 0" description="购物车是空的" />

      <div v-else>
        <el-table :data="cartStore.items" style="width: 100%">
          <el-table-column label="商品">
            <template #default="{ row }">
              <div class="cart-item">
                <img :src="row.image || 'https://picsum.photos/80/80'" class="item-image">
                <div class="item-info">
                  <div class="item-name">{{ row.name }}</div>
                  <div class="item-price">¥{{ row.price }}</div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="单价" width="120">
            <template #default="{ row }">
              ¥{{ row.price }}
            </template>
          </el-table-column>

          <el-table-column label="数量" width="150">
            <template #default="{ row }">
              <el-input-number
                v-model="row.quantity"
                :min="1"
                size="small"
                @change="cartStore.updateQuantity(row.id, row.quantity)"
              />
            </template>
          </el-table-column>

          <el-table-column label="小计" width="120">
            <template #default="{ row }">
              ¥{{ (row.price * row.quantity).toFixed(2) }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button
                type="danger"
                size="small"
                link
                @click="cartStore.removeItem(row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="cart-summary">
          <div class="total">
            <span>总计:</span>
            <span class="total-price">¥{{ cartStore.totalPrice.toFixed(2) }}</span>
          </div>
          <el-button type="primary" size="large" @click="checkout">
            去结算
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()

const checkout = () => {
  ElMessageBox.confirm('确认结算订单吗？', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'info'
  }).then(() => {
    // 跳转到订单确认页面
    router.push('/orders')
  })
}
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

.cart-item {
  display: flex;
  align-items: center;
  gap: 15px;
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

.cart-summary {
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  text-align: right;
}

.total {
  font-size: 18px;
  margin-bottom: 20px;
}

.total-price {
  color: #ff4444;
  font-size: 24px;
  font-weight: bold;
  margin-left: 10px;
}
</style>