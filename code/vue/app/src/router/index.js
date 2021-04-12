import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout1 from '@/views/Layout1.vue'
import Test1 from '@/views/Test1.vue'

Vue.use(VueRouter)

// **** note ****
// routes to be kept alive are configured in a 'keepList'
// array in the component that has the router-view in it

const routes = [
  {
    path: '/cards/',
    name: 'cards-list',
    component: () => import('@/views/Layout1.vue'),
    children: [
      {
        path: 'detail/:cardId/',
        name: 'cards-detail',
        component: () => import('@/components/layout1/CardDetail.vue')
      },
      {
        path: 'nav/:navIndex/',
        name: 'cards-nav',
        component: () => import('@/components/layout1/NavSecondary.vue')
      }
    ]
  },
  {
    path: '/test/',
    name: 'landing',
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
