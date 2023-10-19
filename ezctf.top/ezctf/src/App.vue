<template>
  <div id="app">
    <nav>
      <div>
        <button @click="log()" v-if="!isLogin" id="loginBtn">登录</button>
      </div>
      <router-view/>
      <div id="hiddenInfo" v-if="isLogin">
        <div  @click="showUserInfo()" id="ava">
          <CreateAvatar :username="userInfo.name" />
        </div>
        <div v-if="isHovered" class="user-info">
          <div>
            <CreateAvatar :username="userInfo.name" />
            <p>{{ userInfo.name }}</p>
            <br>
            <div id="ScoreAndTeam">
              <p>积分:&nbsp; {{ userInfo.score }}</p>
              <p>战队：{{ userInfo.team }}</p>
            </div>
          </div>
          <br>
          <button @click="message()" class="board">
            <img src="../src/assets/icon/消息.png" class="icon">&nbsp;消息通知
          </button><br><br>
          <button @click="team()" class="board">
            <img src="../src/assets/icon/战队.png" class="icon">&nbsp;我的战队
          </button><br><br>
          <button @click="superuser()" class="board" v-if="userInfo.isSuperuser">管理系统</button>
          <br v-if="userInfo.isSuperuser"><br v-if="userInfo.isSuperuser">
          <button @click="quit()" class="board">退出登录</button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import CreateAvatar from '../src/components/CreateAvatar.vue';
export default {
  components: {
    CreateAvatar,
  },
  created() {
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
        isLeader: true, //战队队长
        isMember: false, //战队成员
        isSuperuser: true //管理员
      }
    };
  },
  methods: {
    log() {
      this.$router.push("/Log");
    },
    showUserInfo() {
      this.isHovered = !this.isHovered;
    },
    message() {
      
    },
    team() {
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
        const leaderId = this.userInfo.id;
        this.$router.push({ name: 'NoTeam', params: { leaderId } });
      }
    },
    message() {
      this.isHovered = !this.isHovered;
      this.$router.push("/InfoBoard");
    },
    quit() {
      this.userInfo.name='',
      this.userInfo.id='',
      this.userInfo.email='',
      this.userInfo.totalscore='',
      this.userInfo.isLeader=false,
      this.userInfo.isMember=false,
      this.userInfo.isSuperuser=false,
      this.isLogin=false,
      this.isHovered=false
    }
  }
};
</script>

<style>
#app {
  background-color: white;
}

#loginBtn {
    width: 100px;
    height: 50px;
    position: fixed;
    top: 50px;
    right: 150px;
    text-align: center;
}

nav {
  padding: 30px;
}

#ScoreAndTeam {
  margin-left: 60px;
  text-align: left;
}

.user-info {
  position: fixed;
  top: 100px;
  right: 50px;
  width: 15%;
  height: 60%;
  justify-content: center;
  align-items: center;
  background-color: #0d1117;
  padding: 20px;
  text-align: center;
  color:white;
}

#hiddenInfo {
  margin-left: 1000px;
}

.board {
  border: none;
  outline: none;
  box-shadow: none;
  background-color: black;
  width: 100%;
  height: 40px;
  text-align: center;
  color: white;
}

.board:hover {
  background-color: grey;
}

.icon {
  width: 20px;
  height: 20px;
}

#ava {
  position: fixed;
  right: 150px;
  cursor: pointer;
  z-index: 1;
}
</style>
