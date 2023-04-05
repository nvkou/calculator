import Vue from 'vue'
import VueRouter, { Route, RouteConfig } from 'vue-router'
import { dispatchCheckLoggedIn } from '@/store/actions'
import { readIsLoggedIn } from '@/store/getters'
import { store } from '@/store'
import axios from 'axios'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'mainView',
    component: () => import(/* webpackChunkname: "start"*/'../views/MainView.vue'),
    meta: {requireAuth: true},
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
    meta: {requireAuth: false},
  },
  {
    path:'/records',
    name: 'User Records',
    component: () => import('../views/RecordsView.vue'),
    meta: {requireAuth: true}
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// config to check protect view
router.beforeEach(async (to: Route,from,next) =>{
  await dispatchCheckLoggedIn(store);
  const requireAuth = to.meta && to.meta.requireAuth;
  if(!readIsLoggedIn(store) && requireAuth){
    next('/login');
  }else{
    next();
  }
})

axios.interceptors.response.use(
  response =>{
    return response
  },
  error => {
    if (error.response && error.response.status ===401){
      router.push('/login');
    }
    return Promise.reject(error);
  }
)

export default router
