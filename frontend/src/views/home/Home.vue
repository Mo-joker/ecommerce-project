<template>
  <div class="home">
    <!-- 欢迎横幅 -->
    <div class="hero">
      <h1>欢迎来到电商商城</h1>
      <p>发现优质商品，享受购物乐趣</p>
      <el-button type="primary" size="large" @click="router.push('/products')">
        开始购物
      </el-button>
    </div>

    <!-- 热门商品 -->
    <div class="featured-products">
      <div class="container">
        <h2>热门商品</h2>
        <div class="product-grid" v-loading="loading">
          <ProductCard
            v-for="product in products"
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="view-more" v-if="products.length > 0">
          <el-button type="primary" link @click="router.push('/products')">
            查看更多商品
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight } from '@element-plus/icons-vue'
import { productApi } from '@/api/product'
import ProductCard from '@/components/shop/ProductCard.vue'

const router = useRouter()
const loading = ref(false)
const products = ref([])

onMounted(async () => {
  loading.value = true
  try {
    const res = await productApi.getProducts({ limit: 8 })
    products.value = res.items || res
  } catch (error) {
    console.error('获取商品失败', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home {
  min-height: calc(100vh - 120px);
}

/* 欢迎横幅 */
.hero {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 20px;
  font-weight: bold;
}

.hero p {
  font-size: 20px;
  margin-bottom: 30px;
  opacity: 0.9;
}

/* 热门商品区域 */
.featured-products {
  padding: 60px 0;
  background-color: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.featured-products h2 {
  text-align: center;
  font-size: 32px;
  margin-bottom: 40px;
  color: #333;
  position: relative;
}

.featured-products h2:after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background: #409eff;
  margin: 15px auto 0;
  border-radius: 2px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.view-more {
  text-align: center;
  margin-top: 30px;
}

.view-more .el-button {
  font-size: 16px;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 32px;
  }

  .hero p {
    font-size: 16px;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .featured-products h2 {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>