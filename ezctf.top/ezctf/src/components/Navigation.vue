<template>
<div class="topborder">
        <div class="wrap">
        <ul class="header-left">
            <li><a href="#/home" @click="setLoginButtonEnabled(true)"><i class="iconfont icon-xE990"></i>EZCTF</a><span>|</span></li>
            <li><a href="#/ranking" @click="setLoginButtonEnabled(true)"><i class="iconfont icon-paixingbang"></i>Ranking</a></li>
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
            <i id="message" class="iconfont icon-xiaoxi"></i>&nbsp;消息通知
            <p class="sign" v-if="num(messnum)">{{ messnum }}</p>
          </button><br><br>
          <button @click="team()" class="board">
            <i id="team" class="iconfont icon-yusherenyuan"></i>&nbsp;我的战队
          </button><br><br>
          <button @click="setinfo()" class="board" v-if="setInfo"><i id="usersetting" class="iconfont icon-chilun"></i>用户设置</button>
          <button @click="modify()" class="infoBtn" v-if="!setInfo">修改信息</button>
          <button @click="Delete()" class="infoBtn" v-if="!setInfo">注销账号</button>
          <button class="infoBtn" @click="setinfo()" v-if="!setInfo">返回</button>
          <br><br>
          <button @click="quit()" class="board"><i id="logout" class="iconfont icon-guanji"></i>退出登录</button>
        </div>
      </div>
      
    </div>

</template>

<script>
import CreateAvatar from '../components/CreateAvatar.vue';
import { mapState, mapMutations } from 'vuex';
import { logoutUser,user_profile } from '@/UserSystemApi/UserApi';
import { messNum } from '@/UserSystemApi/MessageApi';
export default {
name:'Navigation',
 components: {
    CreateAvatar,
  },
  data() {
      return {
        messnum:'',
      };
  },
  computed: {
    ...mapState([ 'loginButtonEnabled',
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
    ...mapMutations([ 'setLoginButtonEnabled',
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
      localStorage.setItem('LBE',false);
      this.$router.push("/Log");
    },
    showUserInfo() {
      this.setIsHover(!this.$store.state.isHover);
      if(this.$store.state.isHover){
        this.getMessNum();
        this.user_profile();
      }
    },
    setinfo() {
      this.setSetInfo(!this.$store.state.setInfo);
    },
    team() {
      this.setUserInfoButtonEnabled(false);
      this.setInfo=true;
      if(this.$store.state.isLeader&&this.$store.state.teamname){
        this.showUserInfo();
        this.setManageTeam(true);
        this.$router.push("/ManageTeam");
        localStorage.setItem('UBE',false);
      }
      else if(this.$store.state.teamname&&!this.$store.state.isLeader){
        console.log("bug");
        this.showUserInfo();
        this.$router.push("/TeamInfo");
        localStorage.setItem('UBE',false);
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
        localStorage.removeItem('isLogin');
        localStorage.removeItem('username');
        localStorage.removeItem('teamname');
        localStorage.removeItem('score');
        localStorage.removeItem('isLeader');
      })
      .catch((error) => {
        alert(error.response.data.msg);
        console.error('用户退出登录失败', error);
      });
    },
    async getMessNum() {
        try {
          const response = await messNum();
          console.log('未读信息数量响应', response);
          if(response.ret==='success'){
            this.messnum=response.data.unchecked_count;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
    },
    num(a){
      if(a==0)
        return false;
      else
        return true;
    },
    async user_profile() {
      try {
        const response = await user_profile();
        console.log('响应', response);
        if (response.ret === 'success') {
          this.setUsername(response.data.username);
          localStorage.setItem('username', response.data.username);

          this.setTeamname(response.data.team);
          if(response.data.team){
            localStorage.setItem('teamname', response.data.team);
          }
          else{
            localStorage.removeItem('teamname');
          }
          
          this.setScore(response.data.score);
          localStorage.setItem('score', response.data.score);

          this.setIsLeader(response.data.is_leader);
          if(response.data.is_leader){
            localStorage.setItem('isLeader', response.data.is_leader);
          }
          else{
            localStorage.removeItem('isLeader');
          }
        }
      } catch (error) {
        console.error('错误:', error);
      }
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
  font-size: 14px;
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
  width: 15px;
  height: 15px;
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

.sign{
    width: 20px;
    height: 20px;
    position: absolute;
    background-color: red;
    border-radius: 50%;
    text-align: center;
    top:235px;
    right:40px;
  }
  #message{
    font-size: 15px;
  }
  #usersetting{
    font-size: 15px;
  }
  #logout{
    font-size: 15px;
  }
  #team{
    font-size: 15px;
  }
</style>