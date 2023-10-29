<template>
    <div id="registerUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>用户注册</h1>
      <form @submit.prevent="registerUser">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="user.username" required /><br><br>
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="user.password" required /><br><br>
        <label for="password">确认密码:</label>
        <input type="password" id="confirmPassword" v-model="user.confirmPassword" required /><br><br>
        <label for="email">邮箱:</label>
        <input type="email" id="email" v-model="user.email" required /><br><br>
        <button type="submit" @click="userRegister()">注册</button><br><br>
      </form>
    </div>
  </template>
    
  <script>
  import { register } from '../UserSystemApi/UserApi.js';
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        user: {
          username: '',
          password: '',
          confirmPassword:'',
          email: '',
        },
        code: ''
      };
    },
    computed: {
    ...mapState(['loginButtonEnabled','username']),
    },
    methods: {
      ...mapMutations(['setLoginButtonEnabled','setUsername']),
      close() {
        this.setLoginButtonEnabled(true);
        this.$router.push('/Home');
      },
      async Register() {
        try {
          const response = await register( this.user.username, this.user.password, this.user.email);
          alert(response.data.msg);
          console.log('注册响应:', response);
          if (response.return === 'success') {
            this.$router.push("/Log");
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('注册错误:', error);
        }
      },
      userRegister() {
        if(this.user.password==this.user.confirmPassword&&this.user.password!=''){
          this.Register();
        }
        else{
          this.user.password='';
          this.user.confirmPassword='';
          alert("密码设置失败，请重新设置密码！");
        }
      },
    },
  };
  </script>
  
  <style>
  #registerUser {
      margin-top:150px;
      margin-left:440px;
      position: fixed;
      top: auto;
      left: auto;
      width: 500px;
      height: 300px;
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
    