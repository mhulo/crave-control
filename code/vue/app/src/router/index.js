import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from '@/views/Vuetify.vue'
import CardList from '@/views/CardList.vue'
import Layout from '@/views/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'card-list',
    component: CardList
  },
  {
    path: '/layout/',
    name: 'layout',
    component: Layout,
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
