import Vue from 'vue'
import VueRouter from 'vue-router'
import CardList from '../views/CardList.vue'
import Vuetify from '../views/Vuetify.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'card-list',
    component: CardList
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
