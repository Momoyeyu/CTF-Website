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
  data() {
    return {
      isHovered: false,
      setInfo: true,
    };
  },
  computed: {
    ...mapState(['loginButtonEnabled',
                  'userInfoButtonEnabled',
                  'username',
                  'teamname',
                  'score',
                  'isLeader',
                  'isMember',
                  'modifyUser',
                  'deleteUser',
                  'infoboard',
                  'isLogin',
                  'noTeam',
                  'createTeam',
                  'joinTeam',
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
  },
  methods: {
    ...mapMutations(['setLoginButtonEnabled',
                      'setUserInfoButtonEnabled',
                      'setUsername',
                      'setTeamname',
                      'setScore',
                      'setIsLeader',
                      'setIsMember',
                      'setModifyUser',
                      'setDeleteUser',
                      'setInfoBoard',
                      'setIsLogin',
                      'setNoTeam',
                      'setCreateTeam',
                      'setJoinTeam',
    ]),
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
      if(this.userInfo.is_Leader&&!this.userInfo.is_Member){
        this.showUserInfo();
        this.$router.push("/ManageTeam");
      }
      else if(this.userInfo.is_Member){
        this.showUserInfo();
        this.$router.push("/TeamInfo");
      }
      else{
        this.showUserInfo();
        this.setNoTeam(true);
      }
    },
    message() {
      this.isHovered = !this.isHovered;
      this.setUserInfoButtonEnabled(false);
      this.setInfoBoard(true);
    },
    modify() {
      this.setModifyUser(true);
    },
    Delete() {
      this.setDeleteUser(true);
    },
    quit() {
      logoutUser()
      .then((response) => {
        alert(response.msg);
        console.log('用户退出登录成功', response.data);
        this.setUsername('');
        this.setTeamname('None');
        this.setScore('');
        this.setIsLeader(false);
        this.setIsMember(false);
        this.setIsLogin(false);
        this.isHovered=false
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
    border-radius: 15px;
    margin: 0 auto;
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
    left: -80px;
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
  height: 465px;
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