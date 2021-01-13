import Vue from 'vue'
import VueRouter from 'vue-router'
import WidgetList from '../views/WidgetList.vue'
import WidgetShow from '../views/WidgetShow.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'widget-list',
    component: WidgetList
  },
  {
    path: '/widget/:id',
    name: 'widget-show',
    component: WidgetShow,
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
