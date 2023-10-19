<template>
    <div id="loginUser">
      <router-link to="/App" class="close-btn">&#10006;</router-link>
      <h1>用户登录</h1>
      <form @submit.prevent="loginUser">
        <label for="usernameOrEmail">用户名/邮箱:</label>
        <input type="text" id="usernameOrEmail" v-model="loginInfo.usernameOrEmail" required /><br><br>
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="loginInfo.password" required /><br><br>
        <button type="submit" @click="LoginUser()">登录</button><br><br>
        <router-link to="/FP" class="router-link">忘记密码</router-link> |
        <router-link to="/Re" class="router-link">注册</router-link>
      </form>
    </div>
  </template>
    
  <script>
  import { login } from '../UserSystemApi/UserApi.js';
  export default {
    data() {
      return {
        loginInfo: {
          usernameOrEmail: '',
          password:'',
        },
      };
    },
    methods: {
      async LoginUser() {
        try {
          const response = await login(this.loginInfo.usernameOrEmail, this.loginInfo.password);
          console.log('登录响应:', response);
          if (response.return === 'success') {
            this.$router.push({
              path: '/App',
              query: { userInfo_nameAndId: response.userInfo, source: 'Login' } 
            });
          }   
        } catch (error) {
          console.error('登录错误:', error);
        }
      }
    },
  };
  </script>
    
  <style>
  #loginUser {
    margin-top:150px;
    margin-left:450px;
    position: fixed;
    top: auto;
    left: auto;
    width: 30%;
    height: 30%;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
    background-color: #0d1117;
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
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
  }
  </style>