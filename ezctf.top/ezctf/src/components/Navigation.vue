<template>
<div class="topborder">
        <div class="wrap">
        <ul class="header-left">
            <li><a href="#/home"><i class="iconfont">&#xf01ff;</i>Logo</a><span>|</span></li>
            <li><a href="#/ranking"><i class="iconfont">&#xe64b;</i>Ranking</a></li>
        </ul>
        <ul class="header-right">
            <li><button @click="log()" v-if="!isLogin" id="loginBtn" :disabled="!loginButtonEnabled">登录</button></li>
        </ul>
        </div>
              <div id="hiddenInfo" v-if="isLogin">
        <div id="ava">
          <CreateAvatar :username="userInfo.name" />
          <button  @click="showUserInfo()" id="avab"> </button>
        </div>
        <div v-if="isHovered" class="user-info">
          <div>
            <CreateAvatar :username="userInfo.name" />
            <p>{{ userInfo.name }}</p>
            <div id="ScoreAndTeam">
              <p>积分:&nbsp; {{ userInfo.score }}</p>
              <p>战队：{{ userInfo.team }}</p>
            </div>
            <button @click="modify()">修改信息</button> |
            <button>注销账号</button>
          </div>
          <button @click="message()" class="board">
            <img src="../assets/icon/消息.png" class="icon">&nbsp;消息通知
          </button><br><br>
          <button @click="team()" class="board">
            <img src="../assets/icon/战队.png" class="icon">&nbsp;我的战队
          </button><br><br>
          <button @click="superuser()" class="board" v-if="userInfo.isSuperuser">管理系统</button>
          <br v-if="userInfo.isSuperuser"><br v-if="userInfo.isSuperuser">
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
        this.userInfo.name = backInfo.name;
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
        this.userInfo.name = backInfo.name;
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
      userInfo: {
        id: '114',
        name: '于渊龙',
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
    ...mapState(['loginButtonEnabled']),
  },
  methods: {
    ...mapMutations(['setLoginButtonEnabled']),
    log() {
      this.setLoginButtonEnabled(false);
      this.$router.push("/Log");
    },
    showUserInfo() {
      this.isHovered = !this.isHovered;
    },
    team() {
      if(this.userInfo.isLeader&&!this.userInfo.isMember){
        this.showUserInfo();
        const leader = this.userInfo.name;
        this.$router.push({ name: 'ManageTeam', params: { leader } });
      }
      else if(this.userInfo.isMember){
        this.showUserInfo();
        const member = this.userInfo.name;
        this.$router.push({ name: 'TeamInfo', params: { member } });
      }
      else{
        this.showUserInfo();
        const leader = this.userInfo.name;
        this.$router.push({ name: 'NoTeam', params: { leader } });
      }
    },
    message() {
      this.isHovered = !this.isHovered;
      this.$router.push("/InfoBoard");
    },
    modify() {

    },
    quit() {
      logoutUser()
      .then((response) => {
        console.log('用户退出登录成功', response.data);
        this.userInfo.name='',
        this.userInfo.id='',
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
    width:1370px;
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
    width: 60px;
    height: 30px;
    position: relative;
    top: 0px;
    right: 100px;
    text-align: center;
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
  height: 480px;
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

.icon {
  width: 20px;
  height: 20px;
}

#ava {
  position: relative;
  top: 3px;
  right: -200px;
  cursor: pointer;
  z-index: 1;
}
#avab {
  margin-top: 3px;
  margin-left: -50px;
  height: 50px;
  width: 50px;
  border-radius: 50px;
}
</style>