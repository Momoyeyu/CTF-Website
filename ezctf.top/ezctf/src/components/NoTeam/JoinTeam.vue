<template>
    <div id="jointeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>加入战队</h1>
      <input v-model="searchQuery" placeholder="搜索战队" @input="searchTeams" />
      <button @click="searchTeams()">搜索</button><br><br>
      <div class="scrollable-table-container">
        <table class="two-column-table">
          <thead>
            <tr>
            <th>战队名称</th>
            <th>操作</th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="team in filteredTeams" :key="team.id">
              <td>{{ team.name }}</td>
              <td>
                <button @click="jointeam(team.name)">加入</button>
              </td>
              </tr>
          </tbody>
        </table>
      </div><br><br>
      <button @click="Re()">返回</button>
    </div>
  </template>
  
  <script>
  import { joinTeam } from '/src/UserSystemApi/TeamApi.js';
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        name: this.$store.state.username,
        searchQuery: "",
        teams: [
          { id: 1, name: "jwf" },
          { id: 2, name: "yyl" },
          { id: 3, name: "lwk" },
          { id: 4, name: "sjj" },
        ],
      };
    },
    computed: {
      filteredTeams() {
        const query = this.searchQuery.toLowerCase();
        return this.teams.filter((team) => team.name.toLowerCase().includes(query));
      },
      ...mapState(['userInfoButtonEnabled','username','teamname','joinTeam','noTeam']),
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setJoinTeam','setNoTeam']),
      close() {
        this.setUserInfoButtonEnabled(true);
        this.setJoinTeam(false);
      },
      Re() {
        this.setJoinTeam(false);
        this.setNoTeam(true);
      },
      async joinTeamRequest(teamname) {
        try {
          const response = await joinTeam( this.name, teamname);
          if (response.ret === 'success') {
            alert(response.data.msg);
            console.log('成功加入团队:', response.msg);
            this.setJoinTeam(false);
          } else {
            alert(response.data.msg);
            console.error('加入团队失败:', response.msg);
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('网络请求失败:', error);
        }
      },
      async searchTeams() {
        try {
          const response = await searchTeam(this.searchQuery);
          alert(response.data.msg);
          console.log('搜索战队响应', response);
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
#jointeam {
    margin-top:-280px;
    margin-left:400px;
    position: fixed;
    top: auto;
    left: auto;
    width: 500px;
    height: 350px;
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

.two-column-table {
  margin-left: 30%;
  width: 40%;
  table-layout: fixed;
}

.two-column-table th,
.two-column-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.two-column-table th:first-child,
.two-column-table td:first-child {
  text-align: center;
}
</style>
  