<template id="log">
    <div id="loginUser">
    <button @click="close()" class="close-btn">&#10006;</button>
    <h1>用户登录</h1>
    <form>
      <label for="usernameOrEmail">用户名/邮箱:</label>
      <input type="text" id="usernameOrEmail" v-model="loginInfo.usernameOrEmail" required /><br><br>
      <label for="password">密码:</label>
      <input type="password" id="password" v-model="loginInfo.password" required /><br><br>
      <button @click="loginUser()">登录</button><br><br>
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
    ...mapState(['loginButtonEnabled','username','isLogin','log','reg','FoPa','teamname','score','isLeader','isMember']),
    },
    methods: {
      ...mapMutations(['setLoginButtonEnabled','setUsername','setIsLogin','setLog','setReg','setFoPa','setTeamname','setScore','setIsLeader','setIsMember']),
      close() {
        this.setLoginButtonEnabled(true);
        this.$router.push('/');
      },
      async loginUser() {
        try {
          const response = await login(this.loginInfo.usernameOrEmail, this.loginInfo.password);
          console.log('登录响应:', response);
          if (response.ret === 'success') {
            this.$router.push('/'); 
            alert(response.data.msg);
            this.$store.commit('setLoginButtonEnabled', true);
            this.$store.commit('setUsername', response.data.username);
            this.$store.commit('setTeamname', response.data.team_name);
            this.$store.commit('setScore', response.data.score);
            this.$store.commit('setIsLogin', true);
            this.$store.commit('setLog', false);
            if(response.data.team_name =='None') {
              setIsLeader(false);
              setIsMember(false);
            }
            else if(response.data.is_leader){
              setIsLeader(true);
              setIsMember(false);
            }
            else{
              setIsLeader(false);
              setIsMember(true);
            }
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('登录错误:', error);
        }
      },
      Reg() {
        this.setLog(false);
        this.setReg(true);
      },
      FoP() {
        this.setLog(false);
        this.setFoPa(true);
      },
    },
  };
  </script>
    
  <style>
  #loginUser {
    margin-top:200px;
    margin-left:480px;
    position: absolute;
    top: auto;
    left: auto;
    width: 450px;
    height: 250px;
    background-color: #1e1e1e;
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
  </style>