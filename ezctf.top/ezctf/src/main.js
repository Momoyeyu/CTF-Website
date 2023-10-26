<<<<<<< HEAD
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './assets/index_icon/iconfont.css'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
=======
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loginButtonEnabled: true,
    userInfoButtonEnabled: true
  },
  mutations: {
    setLoginButtonEnabled(state, value) {
      state.loginButtonEnabled = value;
    },
    setUserInfoButtonEnabled(state, value) {
      state.userInfoButtonEnabled = value;
    }
  },
});

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')
>>>>>>> 141d1faf8d25c88c882b9bea2cdc41b22d26a9b5
