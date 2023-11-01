import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Ranking from '../views/Ranking.vue'
import Registration from '../views/Registration.vue'
import Login from '../views/Login.vue'
import ForgetPassword from '../views/ForgetPassword.vue'
import ResetPassword from '../views/ResetPassword.vue'
import TeamInfo from '../views/TeamInfo.vue'
import ManageTeam from '../views/ManageTeam.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Home',
    name: 'Home',
    component: Home
  },
  {
    path: '/Ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/Re',
    name: 'Registration',
    component: Registration
  },
  {
    path: '/Log',
    name: 'Login',
    component: Login,
  },
  {
    path: '/FP',
    name: 'ForgetPassword',
    component: ForgetPassword,
  },
  {
    path: '/Reset',
    name: 'ResetPassword',
    component: ResetPassword,
  },
  {
    path: '/TeamInfo',
    name: 'TeamInfo',
    component: TeamInfo,
  },
  {
    path: '/ManageTeam',
    name: 'ManageTeam',
    component: ManageTeam,
  },
]

const router = new VueRouter({
  routes
})

export default router
