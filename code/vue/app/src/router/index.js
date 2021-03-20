import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from '@/views/Vuetify.vue'
import Layout from '@/views/Layout.vue'
import Layout1 from '@/views/Layout1.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home/',
    name: 'layout1',
    component: Layout1,
  },
  {
    path: '/vuetify/',
    name: 'vuetify-hello',
    component: Vuetify,
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
