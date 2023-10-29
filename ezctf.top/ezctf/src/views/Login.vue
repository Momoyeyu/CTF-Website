<template id="log">
    <div id='bkg'>
      <div id="loginUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>用户登录</h1>
      <form @submit.prevent="loginUser">
        <label for="usernameOrEmail">用户名/邮箱:</label>
        <input type="text" id="usernameOrEmail" v-model="loginInfo.usernameOrEmail" required /><br><br>
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="loginInfo.password" required /><br><br>
        <button type="submit" @click="loginUser()">登录</button><br><br>
        <router-link to="/FP" class="router-link">忘记密码</router-link> |
        <router-link to="/Re" class="router-link">注册</router-link>
      </form>
      </div>
    </div>
  </template>
    
  <script>
  import { login } from '../UserSystemApi/UserApi.js';
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        loginInfo: {
          usernameOrEmail: '',
          password:'',
        },
      };
    },
    computed: {
    ...mapState(['loginButtonEnabled','username','isLogin']),
    },
    methods: {
      ...mapMutations(['setLoginButtonEnabled','setUsername','setIsLogin']),
      close() {
        this.setLoginButtonEnabled(true);
        this.$router.push('/Home');
      },
      async loginUser() {
        try {
          const response = await login(this.loginInfo.usernameOrEmail, this.loginInfo.password);
          console.log('登录响应:', response);
          if (response.return === 'success') {
            alert(response.data.msg);
            this.$store.commit('setLoginButtonEnabled', true);
            this.$store.commit('setUsername', response.data.username);
            this.$store.commit('isLogin', true);
            this.$router.push({
              path: '/Home',
              query: { backInfo: response.data, source: 'Login' } 
            });
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('登录错误:', error);
          console.log(error.response);
        }
      }
    },
  };
  </script>
    
  <style>
  #bkg {
    height:100vh;
    width:100%;
    background-image: url('../assets/窗口背景.png');
    background-size: cover;
  }
  #loginUser {
    margin-top:150px;
    margin-left:465px;
    position: fixed;
    top: auto;
    left: auto;
    width: 450px;
    height: 250px;
    background-color: #0d1117;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border-style: solid;
    border-radius: 5px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
  }
  .router-link {
    text-decoration: none;
    color: white;
  }
  .close-btn {
    background: transparent; 
    border: none; 
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
  }
  </style>