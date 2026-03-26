// src/api/product.js
import request from './index'

export const productApi = {
  // 获取商品列表
  async getProducts(params) {
    // 确保 URL 不带尾部斜杠
    const res = await request.get('/products', { params })

    if (res.items && Array.isArray(res.items)) {
      return {
        items: res.items,
        total: res.total || res.items.length
      }
    }

    if (Array.isArray(res)) {
      return {
        items: res,
        total: res.length
      }
    }

    return {
      items: [],
      total: 0
    }
  },

  // 获取商品详情
  async getProduct(id) {
    return await request.get(`/products/${id}`)
  },

  // 获取商品分类
  async getCategories() {
    // 确保 URL 不带尾部斜杠
    const res = await request.get('/products/categories', { params: {} })
    return Array.isArray(res) ? res : (res.categories || [])
  },

  // 创建商品（管理员）
  async createProduct(productData) {
    return await request.post('/products', productData)
  },

  // 更新商品（管理员）
  async updateProduct(id, productData) {
    return await request.put(`/products/${id}`, productData)
  },

  // 删除商品（管理员）
  async deleteProduct(id) {
    return await request.delete(`/products/${id}`)
  }
}