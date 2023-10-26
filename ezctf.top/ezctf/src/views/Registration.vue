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
        <input type="email" id="email" v-model="user.email" required />
        <button type="submit" @click="getEmail()">发送验证码</button><br><br>
        <label for="Vcode">验证码:</label>
        <input type="text" id="Vcode" v-model="code" required /><br><br>
        <button type="submit" @click="userRegister()">注册</button>
        <p>提示：用户名为真实姓名</p><br><br>
      </form>
    </div>
  </template>
    
  <script>
  import { register,validateCode } from '../UserSystemApi/UserApi.js';
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
    ...mapState(['loginButtonEnabled']),
    },
    methods: {
      ...mapMutations(['setLoginButtonEnabled']),
      close() {
        this.setLoginButtonEnabled(true);
        this.$router.push('/Home');
      },
      async getCode() {
        try {
          const response = await register( this.user.username, this.user.password, this.user.email);
          console.log('注册响应:', response);
        } catch (error) {
          console.error('注册错误:', error);
        }
      },
      getEmail() {
        if(this.user.password==this.user.confirmPassword&&this.user.password!=''){
          this.getCode();
        }
        else{
          this.user.password='';
          this.user.confirmPassword='';
          alert("密码设置失败，请重新设置密码！");
        }
      },
      async validateCode() {
        try {
          const response = await validateCode(this.code);
          console.log('验证码响应', response);
          if (response.return === 'success') {
            this.$router.push({
              path: '/Home',
              query: { backInfo: response.userInfo, source: 'Registration' } 
            });
          }
          else{
            alert("注册失败");
          }
        } catch (error) {
          console.error('验证码错误:', error);
        }
      }
    },
  };
  </script>
  
  <style>
  #registerUser {
      margin-top:100px;
      margin-left:440px;
      position: fixed;
      top: auto;
      left: auto;
      width: 500px;
      height: 400px;
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
    