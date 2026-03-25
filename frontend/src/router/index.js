// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/home/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/products/ProductList.vue')
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('@/views/products/ProductDetail.vue')
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/cart/Cart.vue')
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/orders/OrderList.vue')
  },
  {
    path: '/order/:id',
    name: 'OrderDetail',
    component: () => import('@/views/orders/OrderDetail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router