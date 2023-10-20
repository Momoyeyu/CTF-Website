import Vue from 'vue'
import VueRouter from 'vue-router'
import Registration from '../views/Registration.vue'
import Login from '../views/Login.vue'
import ForgetPassword from '../views/ForgetPassword.vue'
import ResetPassword from '../views/ResetPassword.vue'
import NoTeam from '../views/NoTeam/NoTeam.vue'
import CreateTeam from '../views/NoTeam/CreateTeam.vue'
import JoinTeam from '../views/NoTeam/JoinTeam.vue'
import TeamInfo from '../views/TeamInfo.vue'
import ManageTeam from '../views/ManageTeam.vue'
import InfoBoard from '../views/InfoBoard.vue'

Vue.use(VueRouter)

const routes = [
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
    path: '/NoTeam',
    name: 'NoTeam',
    component: NoTeam,
  },
  {
    path: '/CreateTeam',
    name: 'CreateTeam',
    component: CreateTeam,
    props: true,
  },
  {
    path: '/JoinTeam',
    name: 'JoinTeam',
    component: JoinTeam,
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
  {
    path: '/InfoBoard',
    name: 'InfoBoard',
    component: InfoBoard,
  },

]

const router = new VueRouter({
  routes
})

export default router
