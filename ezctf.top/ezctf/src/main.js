import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuex from 'vuex';
import VueCookies from 'vue-cookies'
import './assets/index_icon/iconfont.css'

Vue.use(Vuex);
Vue.use(VueCookies)

Vue.config.productionTip = false
const getCookie = function(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return '';
};

const store = new Vuex.Store({
  state: {
    loginButtonEnabled: true,
    userInfoButtonEnabled: true,
    modifyUser: false,
    deleteUser: false,
    infoBoard: false,
    isLogin: getCookie('isLogin') || false, 
    setInfo: true,
    noTeam: false,
    createTeam: false,
    joinTeam: false,
    deleteTeam: false,
    changeTeamname: false,
    manageTeam: true,
    log: true,
    reg: false,
    FoPa: false,
    RePa: false,
    username: getCookie('username') || '', 
    score: getCookie('score') || '', 
    teamname: getCookie('teamname') || '', 
    isLeader: getCookie('isLeader') || false, 
    isMember: getCookie('isMember') || false, 
    err: '',
  },
  mutations: {
    setLoginButtonEnabled(state, value) {
      state.loginButtonEnabled = value;
    },
    setUserInfoButtonEnabled(state, value) {
      state.userInfoButtonEnabled = value;
    },
    setUsername(state, value) {
      state.username = value;
    },
    setTeamname(state, value) {
      state.teamname = value;
    },
    setScore(state, value) {
      state.score = value;
    },
    setIsLeader(state, value) {
      state.isLeader = value;
    },
    setIsMember(state, value) {
      state.isMember = value;
    },
    setModifyUser(state, value) {
      state.modifyUser = value;
    },
    setDeleteUser(state, value) {
      state.deleteUser = value;
    },
    setInfoBoard(state, value) {
      state.infoBoard = value;
    },
    setIsLogin(state, value){
      state.isLogin = value;
    },
    setSetInfo(state, value){
      state.setInfo = value;
    },
    setNoTeam(state, value){
      state.noTeam =value;
    },
    setCreateTeam(state, value){
      state.createTeam =value;
    },
    setJoinTeam(state, value){
      state.joinTeam =value;
    },
    setDeleteTeam(state, value) {
      state.deleteTeam = value;
    },
    setChangeTeamname(state, value) {
      state.changeTeamname = value;
    },
    setManageTeam(state, value) {
      state.manageTeam = value;
    },
    setLog(state, value){
      state.log =value;
    },
    setReg(state, value){
      state.reg =value;
    },
    setFoPa(state, value){
      state.FoPa =value;
    },
    setRePa(state, value){
      state.RePa =value;
    },
    setErr(state, value){
      state.err =value;
    }
  },
});

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')
