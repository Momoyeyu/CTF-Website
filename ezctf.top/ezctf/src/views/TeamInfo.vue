<template>
    <div id="teaminfo">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>战队信息</h1>
          <p>战队名称:{{ team.name }}</p>
          <p>队长:{{team.leader_id}}&nbsp;&nbsp;&nbsp;得分:1{{ leader_score }}</p>
          <div class="scrollable-table-container">
            <table class="two-column-table">
              <thead>
                <tr>
                <th>成员</th>
                <th>积分</th>
              </tr>
              </thead>
              <tbody>
                <tr v-for="member in members" :key="member.id">
                <td>{{ member.name }}</td>
                <td>{{ member.totalScore }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p>战队成员数:{{team.membernum}}/{{ team.maxnum }}</p>
          <p>战队总积分:{{ team.point }}</p>
        <button @click="quit()">退出战队</button>
    </div>
</template>
    
<script>
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        team: {
          member_name: this.$store.state.username,
          name: this.$store.state.teamname,
          leader_id: 'jwf',
          leader_score: '100',
          membernum: '4',
          maxnum:'10',
          point: '100'
        },
        members: [
        { id: 1, name: 'yyl', totalScore: 100 },
        { id: 2, name: 'lwk', totalScore: 100 },
        { id: 3, name: 'sjj', totalScore: 100 },
        // 添加更多成员
      ],
      };
    },
    computed: {
      ...mapState(['userInfoButtonEnabled','username','teamname']),
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname']),
      close() {
        this.setUserInfoButtonEnabled(true);
        this.$router.push('/Home');
      },
      quit() {
        //发送退出战队请求到后端
          this.$router.push("/Home");
      }
    },
  };
</script>
    
<style>
#teaminfo {
  margin-top:100px;
  margin-left:28%;
  width: 40%;
  position: absolute;
  top: auto;
  left: auto;
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