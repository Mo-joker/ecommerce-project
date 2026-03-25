// src/api/product.js
import request from './index'

export const productApi = {
  // 获取商品列表
  async getProducts(params) {
    try {
      // 转换参数格式
      const apiParams = {
        skip: params.skip || 0,
        limit: params.limit || 12
      }

      if (params.search) apiParams.search = params.search
      if (params.category_id) apiParams.category_id = params.category_id
      if (params.min_price) apiParams.min_price = params.min_price
      if (params.max_price) apiParams.max_price = params.max_price
      if (params.sort && params.sort !== 'default') {
        apiParams.sort = params.sort
      }

      const res = await request.get('/products', { params: apiParams })

      // 处理返回数据格式
      if (res.items && Array.isArray(res.items)) {
        return {
          items: res.items,
          total: res.total,
          page: res.page,
          size: res.size,
          pages: res.pages
        }
      }

      // 如果返回的是数组
      if (Array.isArray(res)) {
        return {
          items: res,
          total: res.length,
          page: 1,
          size: params.limit || 12,
          pages: 1
        }
      }

      return {
        items: [],
        total: 0,
        page: 1,
        size: params.limit || 12,
        pages: 1
      }

    } catch (error) {
      console.error('获取商品列表失败:', error)
      return {
        items: [],
        total: 0,
        page: 1,
        size: params.limit || 12,
        pages: 1
      }
    }
  },

  // 获取商品详情
  async getProduct(id) {
    try {
      const res = await request.get(`/products/${id}`)
      return res
    } catch (error) {
      console.error('获取商品详情失败:', error)
      throw error
    }
  },

  // 获取商品分类
  async getCategories() {
    try {
      const res = await request.get('/products/categories/')
      return Array.isArray(res) ? res : res.categories || []
    } catch (error) {
      console.error('获取分类失败:', error)
      return []
    }
  }
}