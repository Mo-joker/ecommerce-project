// src/api/cart.js
import request from './index'

export const cartApi = {
  // 获取购物车列表
  getCartItems() {
    return request.get('/cart')
  },

  // 添加到购物车
  addToCart(data) {
    return request.post('/cart', data)
  },

  // 更新购物车商品数量
  updateCartItem(itemId, data) {
    return request.put(`/cart/${itemId}`, data)
  },

  // 从购物车移除商品
  removeFromCart(itemId) {
    return request.delete(`/cart/${itemId}`)
  },

  // 清空购物车
  clearCart() {
    return request.delete('/cart')
  }
}
