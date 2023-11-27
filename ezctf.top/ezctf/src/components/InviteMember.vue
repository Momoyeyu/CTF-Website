<template>
    <div id="invitemember">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>邀请成员</h1>
      <label for="search">搜索成员: </label>
      <input id="search" v-model="searchQuery" placeholder="请输入成员名称" @input="filter()"/><br><br>
      <div class="scrollable-table-container">
        <table class="three-column-table">
          <thead>
            <tr>
            <th>用户名</th>
            <th>积分</th>
            <th>操作</th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.username" v-if="!user.team_name">
              <td>{{ user.username }}</td>
              <td>{{ user.score }}</td>
              <td>
                <button @click="invite(user.username)" :disabled="user.team_name">发送邀请</button>
              </td>
              </tr>
          </tbody>
        </table>
      </div><br><br>
      <button id="Return" @click="Re()">返回</button>
    </div>
  </template>
  
  <script>
  import { Invite, teamDetail } from '/src/UserSystemApi/TeamApi.js';
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        searchQuery: "",
        users: [
          {
            username:"",
            score: "",
            leader_email: "",
            team_name:"",
          }
        ],
        maxnum: 10,
      };
    },
    computed: {
      filteredUsers() {
        if(this.searchQuery!=''){
          const query = this.searchQuery.toLowerCase();
          return this.users.filter((user) => user.username.toLowerCase().includes(query));
        }
        else{
          return this.teams;
        }
      },
      ...mapState(['inviteMember','manageTeam','teamname']),
    },
    mounted() {
      this.team_detail("");
    },
    methods: {
      ...mapMutations(['setInviteMember','setManageTeam','setTeamname']),
      close() {
        this.setInviteMember(false);
        this.setManageTeam(true);
      },
      Re() {
        this.setInviteMember(false);
        this.setManageTeam(true);
      },
      async team_detail(name) {
        try {
          const response = await teamDetail(name);
          console.log('获取用户列表响应', response);
          if(response.ret==='success'){
            this.members=response.data.members;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
      },
      async invite(name) {
        try {
          const response = await Invite(name);
          console.log('搜索战队响应', response);
          if(response.ret==='success'){
            alert(response.msg);
            console.log(response.data);
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('错误:', error);
        }
      },
    },
  };
  </script>

<style>
button{
  cursor: pointer;
}
#invitemember {
    position: absolute;
    top: auto;
    left: auto;
    width: 500px;
    height: 360px;
    justify-content: center;
    align-items: center;
    background-color: #1e1e1e;
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
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}

.scrollable-table-container {
  max-height: 300px; 
  overflow-y: auto; 
}

.three-column-table {
  width: 100%;
}

.three-column-table th,
.three-column-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.three-column-table th:first-child,
.three-column-table td:first-child {
  text-align: center;
}

#Return{
  left:250px;
  bottom:20px;
  position: absolute;
}
</style>
  