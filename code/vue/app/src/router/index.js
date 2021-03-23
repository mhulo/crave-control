import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout1 from '@/views/Layout1.vue'
import Test1 from '@/views/Test1.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home/',
    name: 'layout1',
    component: Layout1,
  },
  {
    path: '/test/',
    name: 'test1',
    component: Test1,
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
