<template>
    <div id="jointeam">
      <router-link to="/Home" class="close-btn">&#10006;</router-link>
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
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['user'], 
    data() {
      return {
        username: this.user,
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
    },
    methods: {
      async joinTeamRequest(teamname) {
        try {
          const response = await joinTeam( this.username, teamname);
          if (response.ret === 'success') {
            console.log('成功加入团队:', response.msg);
          } else {
            console.error('加入团队失败:', response.msg);
          }
        } catch (error) {

          console.error('网络请求失败:', error);
        }
      },
      async searchTeams() {
        try {
          const response = await searchTeam(this.searchQuery);
          console.log('搜索战队响应', response);
        } catch (error) {
          console.error('错误:', error);
        }
      },
    },
  };
  </script>

<style>
#jointeam {
    margin-top:10%;
    margin-left:28%;
    position: fixed;
    top: auto;
    left: auto;
    width: 40%;
    height: 40%;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
    background-color: #0d1117;
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
  