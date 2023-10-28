<template>
<div class="topborder">
        <div class="wrap">
        <ul class="header-left">
            <li><a href="#/home"><i class="iconfont icon-weiruan"></i>Logo</a><span>|</span></li>
            <li><a href="#/ranking"><i class="iconfont icon-paixingbang"></i>Ranking</a></li>
        </ul>
        <ul class="header-right">
            <li><button @click="log()" v-if="!isLogin" id="loginBtn" :disabled="!loginButtonEnabled" :class="{ 'disabled-button': !loginButtonEnabled }">登录</button></li>
        </ul>
        </div>
              <div id="hiddenInfo" v-if="isLogin">
        <div id="ava">
          <button  @click="showUserInfo()" :disabled="!userInfoButtonEnabled" id="avab"><CreateAvatar :username="userInfo.name" id="avac"/></button>
        </div>
        <div v-if="isHovered" class="user-info">
          <div>
            <CreateAvatar :username="userInfo.name" />
            <p>{{ userInfo.name }}</p>
            <div id="ScoreAndTeam">
              <p>积分:&nbsp; {{ userInfo.score }}</p>
              <p>战队：{{ userInfo.team }}</p>
            </div>
          </div>
          <br>
          <button @click="message()" class="board">
            <img src="../assets/icon/消息.png" class="icon">&nbsp;消息通知
          </button><br><br>
          <button @click="team()" class="board">
            <img src="../assets/icon/战队.png" class="icon">&nbsp;我的战队
          </button><br><br>
          <button @click="setinfo()" class="board" v-if="setInfo">用户设置</button>
          <button @click="modify()" class="infoBtn" v-if="!setInfo">修改信息</button>
          <button class="infoBtn" v-if="!setInfo">注销账号</button>
          <button class="infoBtn" @click="setinfo()" v-if="!setInfo">返回</button>
          <br><br>
          <button @click="quit()" class="board">退出登录</button>
        </div>
      </div>
    </div>

</template>

<script>
import CreateAvatar from '../components/CreateAvatar.vue';
import { mapState, mapMutations } from 'vuex';
import { logoutUser } from '@/UserSystemApi/UserApi';
export default {
name:'Navigation',
 components: {
    CreateAvatar,
  },
  created() {
    console.log("loginButtonEnabled in created:", this.$store.loginButtonEnabled);
    const backInfo = this.$route.query.backInfo;
    const source = this.$route.query.source;
    if (backInfo && source) {
      if (source === 'Login') {
        this.userInfo.score = backInfo.score;
        this.userInfo.team = backInfo.team_name;
        if(backInfo.team_name =='none') {
          this.userInfo.isLeader=false;
          this.userInfo.isMember=false;
        }
        else if(backInfo.is_leader){
          this.userInfo.isLeader=true;
          this.userInfo.isMember=false;
        }
        else{
          this.userInfo.isLeader=false;
          this.userInfo.isMember=true;
        }
        this.isLogin = true;
      } 
      else if (source === 'Registration') {
        this.userInfo.score = backInfo.score;
        this.userInfo.team = backInfo.team_name;
        if(backInfo.team_name =='none') {
          this.userInfo.isLeader=false;
          this.userInfo.isMember=false;
        }
        else if(backInfo.is_leader){
          this.userInfo.isLeader=true;
          this.userInfo.isMember=false;
        }
        else{
          this.userInfo.isLeader=false;
          this.userInfo.isMember=true;
        }
        this.isLogin = true;
      }
    }
  },
  data() {
    return {
      isLogin: true, //登录状态
      isHovered: false,
      setInfo: true,
      userInfo: {
        name: this.$store.state.username,
        email: '114514@beast.com',
        score: '100',
        team: 'ezctf',
        isLeader: false, //战队队长
        isMember: false, //战队成员
        isSuperuser: true //管理员
      }
    };
  },
  computed: {
    ...mapState(['loginButtonEnabled','userInfoButtonEnabled','username']),
  },
  methods: {
    ...mapMutations(['setLoginButtonEnabled','setUserInfoButtonEnabled','setUsername']),
    log() {
      this.setLoginButtonEnabled(false);
      this.$router.push("/Log");
    },
    showUserInfo() {
      this.isHovered = !this.isHovered;
    },
    setinfo() {
      this.setInfo=!this.setInfo;
    },
    team() {
      this.setUserInfoButtonEnabled(false);
      if(this.userInfo.isLeader&&!this.userInfo.isMember){
        this.showUserInfo();
        this.$router.push("/ManageTeam");
      }
      else if(this.userInfo.isMember){
        this.showUserInfo();
        this.$router.push("/TeamInfo");
      }
      else{
        this.showUserInfo();
        this.$router.push('/NoTeam');
      }
    },
    message() {
      this.isHovered = !this.isHovered;
      this.setUserInfoButtonEnabled(false);
      this.$router.push("/InfoBoard");
    },
    modify() {

    },
    quit() {
      logoutUser()
      .then((response) => {
        console.log('用户退出登录成功', response.data);
        this.setUsername('');
        this.userInfo.email='',
        this.userInfo.totalscore='',
        this.userInfo.isLeader=false,
        this.userInfo.isMember=false,
        this.userInfo.isSuperuser=false,
        this.isLogin=false,
        this.isHovered=false
      })
      .catch((error) => {
        console.error('用户退出登录失败', error);
      });
    }
  }
}
</script>

<style>
.topborder{
    background-color:#1e1e1e;
<<<<<<< HEAD
    width:100%;
=======
    width:1360px;
>>>>>>> 7a01388d7830680134e04f9260f4b0b8393d8c28
    height: 80px;
    line-height: 25px;
    color: #b0b0b0;
    font-size: 26px;
    border-radius: 15px;
}
.topborder .iconfont{
  font-family: "iconfont" !important;
  font-size: 26px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.wrap{
  width: 1300px;
  margin: 0 auto;
}
.header-left{
  padding-left: 0px;
  float: left;
  list-style: none;
}
.header-left span{
  color: #424242;
  margin:0 25px;
}
.header-right{
  list-style: none;
  float: right;
}
.topborder li{
  position: relative;
  float: left;
}
.topborder a{
    color: #bbb;
    text-decoration:none
}
.topborder a:hover{
    color: #fff;
}
#loginBtn {
    border: none;
    outline: none;
    box-shadow: none;
    position: relative;
    top: -10px;
    height: 50px;
    width: 50px;
    border-radius: 50%;
    text-align: center;
    cursor: pointer;
    float: right;
}

.disabled-button {
  background-color: white; 
  color: black;
}

nav {
  padding: 30px;
}

#ScoreAndTeam {
  margin-left: 40px;
  text-align: left;
}

.user-info {
  line-height: 20px;
  position: relative;
  top: 40px;
  right: -105px;
  width: 200px;
  height: 420px;
  justify-content: center;
  align-items: center;
  background-color: #1e1e1e;
  padding: 20px;
  text-align: center;
  color:white;
  border-radius: 5px;
}

#hiddenInfo {
  margin-left: 1000px;
}

.board {
  border: none;
  outline: none;
  box-shadow: none;
  background-color: #1e1e1e;
  width: 100%;
  height: 40px;
  text-align: center;
  color: white;
  border-radius: 5px;
}

.board:hover {
  background-color: grey;
}

.infoBtn {
  border: none;
  outline: none;
  box-shadow: none;
  background-color: #1e1e1e;
  color: white;
  width: 80px;
  height: 30px;
  border-radius: 5px;
}

.infoBtn:hover {
  background-color: grey;
}

.icon {
  width: 20px;
  height: 20px;
}

#ava {
  cursor: pointer;
  z-index: 1;
}
#avab {
  border: none;
  outline: none;
  box-shadow: none;
  position: relative;
  top: 15px;
  right: -200px;
  height: 50px;
  width: 50px;
  border-radius: 50%;
}
#avac {
  position: relative; 
  left: -6px;
  top: -1px;
}
</style>