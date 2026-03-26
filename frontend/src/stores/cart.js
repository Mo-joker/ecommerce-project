import { defineStore } from 'pinia'
import { cartApi } from '@/api/cart'
import { ElMessage } from 'element-plus'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false
  }),

  actions: {
    // 加载购物车（从后端 API）
    async loadCart() {
      this.loading = true
      try {
        const res = await cartApi.getCartItems()
        console.log('购物车数据:', res)
        this.items = Array.isArray(res) ? res : []
      } catch (error) {
        console.error('加载购物车失败:', error)
        this.items = []
      } finally {
        this.loading = false
      }
    },

    // 添加商品到购物车
    async addItem(product, quantity = 1, showMessage = true) {
      try {
        const res = await cartApi.addToCart({
          product_id: product.id,
          quantity: quantity
        })

        // 更新本地状态
        const existing = this.items.find(item => item.product_id === res.product_id)
        if (existing) {
          existing.quantity = res.quantity
        } else {
          this.items.push({
            id: res.id,
            product_id: res.product_id,
            product_name: res.product_name,
            product_price: res.product_price,
            product_image: res.product_image,
            quantity: res.quantity
          })
        }

        if (showMessage) {
          ElMessage.success({
            message: '已添加到购物车',
            duration: 1500
          })
        }
        return true
      } catch (error) {
        console.error('添加失败:', error)
        if (showMessage) {
          ElMessage.error({
            message: '添加失败',
            duration: 2000
          })
        }
        return false
      }
    },

    // 更新购物车商品数量
    async updateQuantity(itemId, quantity) {
      try {
        if (quantity <= 0) {
          await this.removeItem(itemId)
          return
        }

        await cartApi.updateCartItem(itemId, { quantity })

        // 更新本地状态
        const item = this.items.find(item => item.id === itemId)
        if (item) {
          item.quantity = quantity
        }
      } catch (error) {
        console.error('更新失败:', error)
        ElMessage.error('更新失败')
      }
    },

    // 从购物车移除商品
    async removeItem(itemId) {
      try {
        await cartApi.removeFromCart(itemId)

        // 更新本地状态
        const index = this.items.findIndex(item => item.id === itemId)
        if (index !== -1) {
          this.items.splice(index, 1)
        }

        ElMessage.success({
          message: '商品已移除',
          duration: 1500
        })
      } catch (error) {
        console.error('移除失败:', error)
        ElMessage.error({
          message: '移除失败',
          duration: 2000
        })
      }
    },

    // 清空购物车
    async clearCart() {
      try {
        await cartApi.clearCart()
        this.items = []
        ElMessage.success({
          message: '购物车已清空',
          duration: 1500
        })
      } catch (error) {
        console.error('清空失败:', error)
        ElMessage.error({
          message: '清空失败',
          duration: 2000
        })
      }
    },

    // 清空购物车（不显示消息，用于结算后）
    async clearCartWithoutMessage() {
      try {
        await cartApi.clearCart()
        this.items = []
      } catch (error) {
        console.error('清空失败:', error)
      }
    }
  },

  getters: {
    totalItems: (state) => {
      return state.items.reduce((sum, item) => sum + item.quantity, 0)
    },

    totalPrice: (state) => {
      return state.items.reduce((sum, item) => sum + (item.product_price * item.quantity), 0)
    }
  }
})