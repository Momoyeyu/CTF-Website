<template id="log">
    <div id="loginUser">
    <button @click="close()" class="close-btn">&#10006;</button>
    <h1 style="margin-bottom: -5px;">用户登录</h1>
    <p v-if="err" id="er">{{ err }}</p>
    <br v-if="!err">
    <br v-if="!err">
    <form @submit.prevent="loginUser()">
      <div class="uniquecontainer">
      <label for="usernameOrEmail">用户名/邮箱:</label><br>
      <input type="text" id="usernameOrEmail" v-model="loginInfo.usernameOrEmail" required /><br><br>
      </div>
      <div class="uniquecontainer">
      <label  for="password">密码:</label><br>
      <input type="password" id="password" v-model="loginInfo.password" required /><br><br>
      </div>  
      <button class="uniquebutton" type="submit">登录</button><br><br>
      <button @click="FoP()" class="btn">忘记密码</button> |
      <button @click="Reg()" class="btn">注册</button>
    </form>
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
    ...mapState(['loginButtonEnabled','username','isLogin','log','reg','FoPa','teamname','score','isLeader','isMember','err']),
    },
    methods: {
      ...mapMutations(['setLoginButtonEnabled','setUsername','setIsLogin','setLog','setReg','setFoPa','setTeamname','setScore','setIsLeader','setIsMember','setErr']),
      close() {
        this.setLoginButtonEnabled(true);
        this.setErr("");
        this.$router.push('/');
      },
      async loginUser() {
        try {
          const response = await login(this.loginInfo.usernameOrEmail, this.loginInfo.password);
          console.log('登录响应:', response);
          if (response.ret === 'success') {
            this.$router.push('/');
            this.setLoginButtonEnabled(true);
            this.setUsername(response.data.username);
            localStorage.setItem('username', response.data.username);

            this.setTeamname(response.data.team_name);
            if (response.data.team_name) {
              localStorage.setItem('teamname', response.data.team_name);
            }

            this.setScore(response.data.score);
            localStorage.setItem('score', response.data.score);

            this.setIsLogin(true);
            localStorage.setItem('isLogin', 'true');
            
            this.setErr("");

            this.setIsLeader(response.data.is_leader);
            if(response.data.is_leader){
              localStorage.setItem('isLeader', response.data.is_leader);
            }
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
          console.error('登录错误:', error);
        }
      },
      Reg() {
        this.setLog(false);
        this.setReg(true);
        this.setErr("");
      },
      FoP() {
        this.setLog(false);
        this.setFoPa(true);
        this.setErr("");
      },
    },
  };
  </script>
    
  <style>
  #loginUser {
    position: absolute;
    top: auto;
    left: auto;
    width: 450px;
    height: 360px;
    background-color: #1e1e1e;
    justify-content: center;
    align-items: center;
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
  .btn{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 80px;
    height: 40px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn:hover{
    background-color: grey;
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