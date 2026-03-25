// src/api/order.js
import request from './index'

export const orderApi = {
  // 获取订单列表
  getOrders(params) {
    return request.get('/orders', { params })
  },

  // 获取订单详情
  getOrder(id) {
    return request.get(`/orders/${id}`)
  },

  // 创建订单
  createOrder(data) {
    return request.post('/orders', data)
  },

  // 更新订单状态
  updateOrderStatus(id, status) {
    return request.put(`/orders/${id}/status`, null, { params: { status } })
  }
}