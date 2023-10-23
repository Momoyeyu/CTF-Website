import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loginButtonEnabled: true,
  },
  mutations: {
    setLoginButtonEnabled(state, value) {
      state.loginButtonEnabled = value;
    },
  },
});

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')
