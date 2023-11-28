<template>
    <div id="registerUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1 style="margin-bottom: -5px;">用户注册</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <br v-if="!err">
      <div>
        <div class="uniquecontainer">
        <label for="username">用户名:</label><br>
        <input type="text" id="username" v-model="user.username" required /><br><br>
       </div>
        <div class="uniquecontainer">
        <label for="password">密码:</label><br>
        <input type="password" id="password" v-model="user.password" required /><br><br>
        </div>
        <div class="uniquecontainer">
        <label for="password">确认密码:</label><br>
        <input type="password" id="confirmPassword" v-model="user.confirmPassword" required /><br><br>
        </div>
        <div class="uniquecontainer">
        <label for="email">邮箱:</label><br>
        <input type="email" id="email" v-model="user.email" required /><br>
        </div>
        <div class="uniquecontainer">
        <label for="username">验证码:</label><br>
        <input type="text" id="code" v-model="code" required /><br>
        <button style="margin-top: 5px;" @click="Register()">获取验证码</button><br><br>
        </div>
        <button @click="ValidateCode()" class="uniquebutton" type="submit" :disabled="!btn">注册</button><br><br>
      </div>
    </div>
  </template>
    
  <script>
  import { register,validateCode,login } from '../UserSystemApi/UserApi.js';
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
        code: '',
        btn: false,
      };
    },
    computed: {
    ...mapState(['loginButtonEnabled','username','reg','log','err','isLogin','teamname','score','isLeader','isMember',]),
    },
    methods: {
      ...mapMutations(['setLoginButtonEnabled','setUsername','setReg','setLog','setErr','setIsLogin','setTeamname','setScore','setIsLeader','setIsMember',]),
      close() {
        this.btn=false;
        this.setLoginButtonEnabled(true);
        this.setReg(false);
        this.setLog(true);
        this.setErr("");
      },
      async Register() {
        try {
          const response = await register( this.user.username, this.user.password, this.user.email);
          console.log('注册响应:', response);
          if (response.ret === 'success') {
            this.setErr("");
            alert(response.msg);
            this.btn=true;
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
          console.error('注册错误:', error);
        }
      },
      registerUser() {
        if(this.user.password==this.user.confirmPassword&&this.user.password!=''){
          this.Register();
        }
        else{
          this.user.password='';
          this.user.confirmPassword='';
          alert("密码设置失败，请重新设置密码！");
        }
      },
      async ValidateCode() {
        try {
          const response = await validateCode( this.user.username, this.code);
          alert(response.msg);
          console.log('注册响应:', response);
          if (response.ret === 'success') {
            this.loginUser();
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
          console.error('注册错误:', error);
        }
      },
      async loginUser() {
        try {
          const response = await login(this.user.username, this.user.password);
          console.log('登录响应:', response);
          if (response.ret === 'success') {
            this.$router.push('/'); 
            this.setLoginButtonEnabled(true);
            this.setLog(true);
            this.setReg(false);
            this.setUsername(response.data.username);
            document.cookie = `username=${response.data.username}; path=/`;
            this.setTeamname(response.data.team_name);
            if(response.data.team_name){
              document.cookie = `teamname=${response.data.team_name}; path=/`;
            }
            this.setScore(response.data.score);
            document.cookie = `score=${response.data.score}; path=/`;
            this.setIsLogin(true);
            document.cookie = `isLogin=${true}; path=/`;
            this.setErr("");
            this.btn=false;
            this.$store.commit('setReg', false);
            this.$store.commit('setLog', true);        
            if(response.data.team_name&&!response.data.is_leader) {
              this.setIsLeader(false);
              document.cookie = `isLeader=${false}; path=/`;
              this.setIsMember(true);
              document.cookie = `isMember=${true}; path=/`;
            }
            else if(response.data.is_leader){
              this.setIsLeader(true);
              document.cookie = `isLeader=${true}; path=/`;
              this.setIsMember(false);
              document.cookie = `isMember=${false}; path=/`;
            }
            else{
              this.setIsLeader(false);
              document.cookie = `isLeader=${false}; path=/`;
              this.setIsMember(false);
              document.cookie = `isMember=${false}; path=/`;
            }
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
          console.error('登录错误:', error);
        }
      },
    },
  };
  </script>
  
  <style>
  #registerUser {
      position: absolute;
      top: 20%;
      left: auto;
      width: 500px;
      height: 550px;
      justify-content: center;
      align-items: center;
      background-color: #1e1e1e;
      padding: 20px;
      border-style: solid;
      border-radius: 20px;
      border-color:white;
      border-width: 5px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      text-align: center;
      color:white;
  }
  .uniquecontainer label{
    float: left;
    margin-left:10px;
    margin-bottom: 2px;
  }
  .uniquecontainer input{
    border-top: transparent;
    border-left: transparent;
    border-right: transparent;
    border-bottom: 2px solid #fff;
    background-color: transparent;
    height: 25px;
    width: 220px;
    font-size: 20px;
    color: #fff;
  }
  .uniquecontainer input:focus{   
    outline: none;
    border-top: transparent;
    border-left: transparent;
    border-right: transparent;
    border-bottom: 2px solid #fff;
    background-color: transparent;
    height: 25px;
    width: 220px;
    font-size: 20px;
    color: #fff;
  }
  .uniquecontainer {  
    width: 250px;
    background-color: #555;
    margin: 0 auto;
    margin-bottom:5px;
    border-radius: 5px;
    padding-top: 5px;
  }
  .uniquebutton{
    width: 70px;
    height: 35px;
    font-size: 16px;
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
  #er{
    padding: 4px;
    color:red;
    font-size: small;
  }
  </style>
    