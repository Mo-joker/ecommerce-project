<template>
  <div class="product-list-page">
    <div class="container">
      <!-- 筛选栏 -->
      <div class="filter-section">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索商品"
          :prefix-icon="Search"
          style="width: 250px"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        />

        <el-select
          v-model="selectedCategory"
          placeholder="商品分类"
          clearable
          style="width: 150px"
          @change="handleFilter"
        >
          <el-option
            v-for="cat in categories"
            :key="cat.id"
            :label="cat.name"
            :value="cat.id"
          />
        </el-select>

        <div class="price-range">
          <el-input-number
            v-model="minPrice"
            :min="0"
            placeholder="最低价"
            style="width: 120px"
            controls-position="right"
            @change="handleFilter"
          />
          <span>-</span>
          <el-input-number
            v-model="maxPrice"
            :min="0"
            placeholder="最高价"
            style="width: 120px"
            controls-position="right"
            @change="handleFilter"
          />
        </div>

        <div class="sort-select">
          <el-select v-model="sortBy" placeholder="排序方式" style="width: 140px" @change="handleFilter">
            <el-option label="默认排序" value="default" />
            <el-option label="价格从低到高" value="price_asc" />
            <el-option label="价格从高到低" value="price_desc" />
          </el-select>
        </div>
      </div>

      <!-- 商品列表 - 网格布局 -->
      <div class="product-grid" v-loading="loading">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>

      <!-- 分页组件 -->
      <div class="pagination-wrapper" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 36, 48]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>

      <!-- 空状态 -->
      <el-empty v-if="!loading && products.length === 0" description="暂无商品" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { productApi } from '@/api/product'
import ProductCard from '@/components/shop/ProductCard.vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const products = ref([])
const categories = ref([])
const total = ref(0)

// 筛选条件
const searchKeyword = ref('')
const selectedCategory = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)
const sortBy = ref('default')
const currentPage = ref(1)
const pageSize = ref(12)

// 加载商品分类
const loadCategories = async () => {
  try {
    const res = await productApi.getCategories()
    categories.value = res
  } catch (error) {
    console.error('加载分类失败', error)
  }
}

// 加载商品列表
const loadProducts = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      search: searchKeyword.value || undefined,
      category_id: selectedCategory.value || undefined,
      min_price: minPrice.value || undefined,
      max_price: maxPrice.value || undefined,
      sort: sortBy.value !== 'default' ? sortBy.value : undefined
    }

    const res = await productApi.getProducts(params)
    products.value = res.items || []
    total.value = res.total || 0

  } catch (error) {
    console.error('加载商品失败:', error)
    ElMessage.error('加载商品失败，请刷新重试')
    products.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 处理筛选
const handleFilter = () => {
  currentPage.value = 1
  loadProducts()
  updateUrlParams()
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  loadProducts()
  updateUrlParams()
}

// 处理页码变化
const handlePageChange = (page) => {
  currentPage.value = page
  loadProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
  updateUrlParams()
}

// 处理每页数量变化
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadProducts()
  updateUrlParams()
}

// 更新URL参数
const updateUrlParams = () => {
  const params = {}
  if (searchKeyword.value) params.q = searchKeyword.value
  if (selectedCategory.value) params.cat = selectedCategory.value
  if (minPrice.value) params.min = minPrice.value
  if (maxPrice.value) params.max = maxPrice.value
  if (sortBy.value !== 'default') params.sort = sortBy.value
  if (currentPage.value > 1) params.page = currentPage.value
  if (pageSize.value !== 12) params.size = pageSize.value

  router.replace({ query: params })
}

// 从URL读取参数
const readUrlParams = () => {
  const query = route.query
  if (query.q) searchKeyword.value = query.q
  if (query.cat) selectedCategory.value = parseInt(query.cat)
  if (query.min) minPrice.value = parseFloat(query.min)
  if (query.max) maxPrice.value = parseFloat(query.max)
  if (query.sort) sortBy.value = query.sort
  if (query.page) currentPage.value = parseInt(query.page)
  if (query.size) pageSize.value = parseInt(query.size)
}

onMounted(() => {
  readUrlParams()
  loadCategories()
  loadProducts()
})
</script>

<style scoped>
.product-list-page {
  min-height: calc(100vh - 120px);
  background-color: #f5f5f5;
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.filter-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: center;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-select {
  margin-left: auto;
}

/* 商品网格布局 - 一行3个 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
  min-height: 400px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  background: white;
  border-radius: 8px;
}

/* 响应式布局：在平板设备上显示2个 */
@media (max-width: 992px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
}

/* 在手机设备上显示1个 */
@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .sort-select {
    margin-left: 0;
  }

  .price-range {
    justify-content: space-between;
  }

  .product-grid {
    grid-template-columns: repeat(1, 1fr);
    gap: 15px;
  }
}
</style>