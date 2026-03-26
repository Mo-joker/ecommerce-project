<template>
  <div class="product-list-page">
    <div class="container">
      <!-- 管理员操作栏 -->
      <div v-if="isAdmin" class="admin-bar">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          添加商品
        </el-button>
      </div>

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

      <!-- 商品列表 -->
      <div v-loading="loading" class="product-grid">
        <template v-if="!loading && products.length > 0">
          <div v-for="product in products" :key="product.id" class="product-card-wrapper">
            <ProductCard :product="product" />
            <!-- 管理员操作按钮 -->
            <div v-if="isAdmin" class="admin-actions">
              <el-button type="primary" size="small" @click="showEditDialog(product)">编辑</el-button>
              <el-popconfirm title="确定要删除这个商品吗？" @confirm="handleDelete(product.id)">
                <template #reference>
                  <el-button type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </template>

        <div v-if="!loading && products.length === 0" class="empty-state">
          <el-empty description="暂无商品" />
        </div>
      </div>
    </div>

    <!-- 添加/编辑商品对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑商品' : '添加商品'"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="productForm" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入商品名称" />
        </el-form-item>

        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="productForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入商品描述"
          />
        </el-form-item>

        <el-form-item label="价格" prop="price">
          <el-input-number v-model="productForm.price" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>

        <el-form-item label="库存" prop="stock">
          <el-input-number v-model="productForm.stock" :min="0" style="width: 100%" />
        </el-form-item>

        <el-form-item label="商品分类" prop="category_id">
          <el-select v-model="productForm.category_id" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="商品图片" prop="image_url">
          <el-input v-model="productForm.image_url" placeholder="请输入图片 URL（选填）" />
        </el-form-item>

        <el-form-item label="是否上架" prop="is_active">
          <el-switch v-model="productForm.is_active" active-text="上架" inactive-text="下架" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, Plus } from '@element-plus/icons-vue'
import { productApi } from '@/api/product'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import ProductCard from '@/components/shop/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const products = ref([])
const categories = ref([])

// 管理员权限
const isAdmin = computed(() => {
  if (!userStore.userInfo && userStore.token) {
    userStore.getUserInfo()
  }
  return userStore.userInfo?.is_admin || false
})

// 筛选条件
const searchKeyword = ref('')
const selectedCategory = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)
const sortBy = ref('default')

// 对话框相关
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const productForm = ref({
  id: null,
  name: '',
  description: '',
  price: 0,
  stock: 0,
  category_id: null,
  image_url: '',
  is_active: true
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择商品分类', trigger: 'change' }]
}

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
  if (loading.value) return

  loading.value = true
  try {
    const params = {
      skip: 0,
      limit: 100,
      search: searchKeyword.value || undefined,
      category_id: selectedCategory.value || undefined,
      min_price: minPrice.value || undefined,
      max_price: maxPrice.value || undefined,
      sort: sortBy.value !== 'default' ? sortBy.value : undefined
    }

    const res = await productApi.getProducts(params)
    products.value = res.items || []

  } catch (error) {
    console.error('加载商品失败:', error)
    ElMessage.error('加载商品失败')
    products.value = []
  } finally {
    loading.value = false
  }
}

// 监听路由变化，确保每次进入页面都重新加载数据
watch(() => route.path, (newPath, oldPath) => {
  if (newPath === '/products' && newPath !== oldPath) {
    loadProducts()
    loadCategories()
  }
})

// 显示添加对话框
const showAddDialog = () => {
  isEdit.value = false
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (product) => {
  isEdit.value = true
  productForm.value = {
    id: product.id,
    name: product.name,
    description: product.description,
    price: product.price,
    stock: product.stock,
    category_id: product.category_id,
    image_url: product.image_url || '',
    is_active: product.is_active
  }
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  productForm.value = {
    id: null,
    name: '',
    description: '',
    price: 0,
    stock: 0,
    category_id: null,
    image_url: '',
    is_active: true
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value) {
          await productApi.updateProduct(productForm.value.id, productForm.value)
          ElMessage.success('商品更新成功')
        } else {
          await productApi.createProduct(productForm.value)
          ElMessage.success('商品创建成功')
        }
        dialogVisible.value = false
        loadProducts()
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 删除商品
const handleDelete = async (id) => {
  try {
    await productApi.deleteProduct(id)
    ElMessage.success('商品已删除')
    loadProducts()
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

// 处理筛选和搜索
const handleFilter = () => {
  loadProducts()
}

const handleSearch = () => {
  loadProducts()
}

onMounted(() => {
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

.admin-bar {
  margin-bottom: 20px;
  text-align: right;
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

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  min-height: 400px;
}

@media (max-width: 992px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}

.product-card-wrapper {
  position: relative;
}

.admin-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.empty-state {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

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
}
</style>