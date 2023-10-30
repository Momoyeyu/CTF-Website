import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuex from 'vuex';
import './assets/index_icon/iconfont.css'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loginButtonEnabled: true,
    userInfoButtonEnabled: true,
    modifyUser: false,
    deleteUser: false,
    infoBoard: false,
    isLogin: false,
    noTeam: false,
    createTeam: false,
    joinTeam: false,
    username: '',
    teamname: '',
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
    setNoTeam(state, value){
      state.noTeam =value;
    },
    setCreateTeam(state, value){
      state.createTeam =value;
    },
    setJoinTeam(state, value){
      state.joinTeam =value;
    }
  },
});

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')
