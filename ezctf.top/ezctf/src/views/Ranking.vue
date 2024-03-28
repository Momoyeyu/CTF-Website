<template>
<div class="rank">
  <div class="user-rank">
    <div class="rank-head">
    <h1>用户排行榜</h1>
    </div>
    <div class="rank-body">
        <table class="rank-table">
            <tr v-if="this.fetchMy" class="Myrank-title">
                <td>我的排名</td>
                <td>姓名</td>
                <td>积分</td>
                <td>上次提交</td>
            </tr>
            <tr v-if="this.fetchMy" class="Myrank-body">
                <td v-if="fetchMy">#{{ fetchMy.rank }}</td>
                <td>{{ fetchMy.username }}</td>
                <td>{{ fetchMy.score}}</td>
                <td>{{ fetchMy.last_commit }}</td>
            </tr>
            <tr class="table-title">
                <td>总排名</td>
                <td>姓名</td>
                <td>积分</td>
                <td>上次提交</td>
            </tr>
            <tr v-for="item in sortedUsers" :key="item.rank">
                <td>#{{ item.rank }}</td>
                <td>{{ item.username }}</td>
                <td>{{ item.score }}</td>
                <td>{{ item.last_commit }}</td>
            </tr>
        </table>
    </div>
  </div>
  <div class="team-rank">
    <div class="rank-head">
    <h1>战队排行榜</h1>
    </div>
    <div class="rank-body">
        <table class="rank-table">
          <tr v-if="this.fetchMyteam" class="Myrank-title">
                <td>排名</td>
                <td>队名</td>
                <td>队伍人数</td>
                <td>总积分</td>
            </tr>
            <tr v-if="this.fetchMyteam" class="Myrank-body">
                <td>#{{ fetchMyteam.rank }}</td>
                <td>{{ fetchMyteam.team_name }}</td>
                <td>{{ fetchMyteam.member_count}}</td>
                <td>{{ fetchMyteam.score }}</td>
            </tr>
            <tr class="table-title">
                <td>排名</td>
                <td>队名</td>
                <td>队伍人数</td>
                <td>总积分</td>
            </tr>
            <tr v-for="item in sortedTeams" :key="item.team_id">
                <td>#{{ item.rank }}</td>
                <td>{{ item.team_name }}</td>
                <td>{{ item.member_count }}</td>
                <td>{{ item.score }}</td>
            </tr>
        </table>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
export default {
name:'Ranking',
data(){
    return{
        users: [],
        teams: [],  
    }
},
methods: {  
    fetchUsersData() {  
      axios.get('/api/rank/user') 
        .then(response => {  
          this.users = response.data.data.user_list;  
          console.log(this.users);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    },
    fetchTeamsData() {  
      axios.get('/api/rank/team') 
        .then(response => {  
          this.teams = response.data.data.team_list;  
          console.log(this.teams);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    },
  }, 
  mounted() {  
    this.fetchUsersData();  
    this.fetchTeamsData();  
  }, 
computed: {  
  ...mapState(['isLogin']),
  ...mapState(['username']),
  ...mapState(['teamname']),
  ...mapState(['isLeader']),
  ...mapState(['isMember']),
    fetchMy() {  
      let result = this.sortedUsers.find(obj => obj.username === this.username);   
      if (result) {  
        return result;  
      } else {  
        return false;  
      }  
    },  
    fetchMyteam() {  
      let result = this.sortedTeams.find(obj => obj.team_name === this.teamname);  
      if (result) {  
        return result;  
      } else {  
        return false;  
      }  
    }, 
    sortedUsers() { //页面加载完成后自动对数据进行排序并生成排名
      return this.users.sort((a, b) => b.score - a.score).map((item, index) => ({  
        ...item,  
        rank: index + 1,  
      }));  
    }, 
    sortedTeams() {  
      return this.teams.sort((a, b) => b.score - a.score).map((item, index) => ({  
        ...item,  
        rank: index + 1,  
      })); 
    },
},
}
</script>

<style>
.rank{
  width: 1300px;
  margin: 15px auto;
  color: #fff;
}
.user-rank{
    width: 550px;
    float: left;
    padding: 8px;
    background-color: #bbb;
    border-radius: 10px;
}
.team-rank{
    width: 550px;
    float: right;
    padding: 8px;
    background-color: #bbb;
    border-radius: 10px;
}
.rank h1 {
    text-align: center;
    margin-top: 0px;
    margin-bottom: 0px;
    padding-top :20px;
    padding-bottom :20px;
    background-color: #1f6feb;
}
.rank-head{
  width: 100%;
  background-color: #161b22;
}
.rank-body{
  width: 100%;
  background-color: #161b22;
}
.rank-table{
    width: 100%;  
    border-collapse: collapse;  
}
.rank-table tr{
    border-top: 2px solid #cbc;
}
.rank-table td{
width: 25%;
text-align: center;
line-height: 50px;
}
</style>