<template>
<div class="topborder">
        <div class="wrap">
        <ul class="header-left">
            <li><a href="#/home"><i class="iconfont icon-xE990"></i>EZCTF</a><span>|</span></li>
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
        <div v-if="isHover" class="user-info">
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
          <button @click="Delete()" class="infoBtn" v-if="!setInfo">注销账号</button>
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
  computed: {
    ...mapState(['loginButtonEnabled',
                  'userInfoButtonEnabled',
                  'isHover',
                  'username',
                  'teamname',
                  'score',
                  'isLeader',
                  'isMember',
                  'modifyUser',
                  'deleteUser',
                  'setInfo',
                  'infoboard',
                  'isLogin',
                  'noTeam',
                  'createTeam',
                  'joinTeam',
                  'manageTeam',
    ]),
    userInfo() {
      return {
        name: this.$store.state.username, 
        score: this.$store.state.score,
        team: this.$store.state.teamname, 
        is_Leader: this.$store.state.isLeader,
        is_Member: this.$store.state.isMember,
      };
    },
    isHover: {
      get() {
        return this.$store.state.isHover;
      },
      set(value) {
        this.setIsHover(value);
      }
    },
    setInfo: {
      get() {
        return this.$store.state.setInfo;
      },
      set(value) {
        this.setSetInfo(value);
      }
    },
  },
  methods: {
    ...mapMutations(['setLoginButtonEnabled',
                      'setUserInfoButtonEnabled',
                      'setIsHover',
                      'setUsername',
                      'setTeamname',
                      'setScore',
                      'setIsLeader',
                      'setIsMember',
                      'setModifyUser',
                      'setDeleteUser',
                      'setSetInfo',
                      'setInfoBoard',
                      'setIsLogin',
                      'setNoTeam',
                      'setCreateTeam',
                      'setJoinTeam',
                      'setManageTeam'
    ]),
    log() {
      this.setLoginButtonEnabled(false);
      this.$router.push("/Log");
    },
    showUserInfo() {
      this.setIsHover(!this.$store.state.isHover);
    },
    setinfo() {
      this.setSetInfo(!this.$store.state.setInfo);
    },
    team() {
      this.setUserInfoButtonEnabled(false);
      this.setInfo=true;
      console.log(this.userInfo.is_Member);
      if(this.userInfo.is_Leader&&!this.userInfo.is_Member){
        this.showUserInfo();
        this.setManageTeam(true);
        this.$router.push("/ManageTeam");
      }
      else if(this.userInfo.is_Member){
        console.log(this.userInfo.is_Member);
        console.log("bug");
        this.showUserInfo();
        this.$router.push("/TeamInfo");
      }
      else{
        this.showUserInfo();
        this.setNoTeam(true);
      }
    },
    message() {
      this.setIsHover(!this.$store.state.isHover);
      this.setInfo=true;
      this.setUserInfoButtonEnabled(false);
      this.setInfoBoard(true);
    },
    modify() {
      this.setModifyUser(true);
      this.setIsHover(false);
      this.setUserInfoButtonEnabled(false);
    },
    Delete() {
      this.setDeleteUser(true);
      this.setIsHover(false);
      this.setUserInfoButtonEnabled(false);
    },
    quit() {
      logoutUser()
      .then((response) => {
        console.log('用户退出登录成功', response.data);
        this.setUsername('');
        this.setTeamname('');
        this.setScore('');
        this.setIsLeader(false);
        this.setIsMember(false);
        this.setIsLogin(false);
        this.setIsHover(false);
        document.cookie = "isLogin=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        document.cookie = "teamname=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        document.cookie = "score=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        document.cookie = "isLeader=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        document.cookie = "isMember=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      })
      .catch((error) => {
        alert(error.response.data.msg);
        console.error('用户退出登录失败', error);
      });
    }
  }
}
</script>

<style>
.topborder{
    background-color:#1e1e1e;
    width:1600px;
    height: 80px;
    line-height: 25px;
    color: #b0b0b0;
    font-size: 26px;
    border: 1px solid #161b22;
    border-radius: 15px;
    margin: 0 auto;
    margin-top: 5px;
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
  float: left;
  letter-spacing: 0.05em;
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
    top: -11px;
    left: -200px;
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
  font-size: large;
}

.user-info {
  line-height: 20px;
  position: relative;
  top: 40px;
  right: -105px;
  width: 200px;
  height: 450px;
  justify-content: center;
  align-items: center;
  background-color: #1e1e1e;
  padding: 20px;
  text-align: center;
  color:white;
  border-radius: 5px;
  z-index: 1000;
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
  height: 20px;
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