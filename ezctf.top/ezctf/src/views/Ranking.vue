<template>
<div class="rank">
  <div class="user-rank">
    <div class="rank-head">
    <h1>用户排行榜</h1>
    </div>
    <div class="rank-body">
        <table class="rank-table">
            <tr class="table-title">
                <td>排名</td>
                <td>姓名</td>
                <td>得分</td>
                <td>上次提交</td>
            </tr>
            <tr v-for="item in sortedUsers" :key="item.score">
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
      axios.get('http://localhost:80/api/rank/user') 
        .then(response => {  
          this.users = response.data.data.user_list;  
          console.log(this.users);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    },
    fetchTeamsData() {  
      axios.get('http://localhost:80/api/rank/team') 
        .then(response => {  
          this.teams = response.data.data.team_list;  
          console.log(this.teams);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    }  
  }, 
  mounted() {  
    // 在组件挂载完成后发送请求获取数据  
    this.fetchUsersData();  
    this.fetchTeamsData();  
  }, 
computed: {  //页面加载完成后自动对数据进行排序并生成排名
    sortedUsers() { 
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
    } ,
},
}
</script>

<style>
.rank{
  width: 1300px;
  margin: 15px auto;
  background-color:aqua;
  color: #fff;
}
.user-rank{
    width: 550px;
    float: left;
    padding: 10px;
    background-color: #bbb;
    border-radius: 10px;
}
.team-rank{
    width: 550px;
    float: right;
    padding: 10px;
    background-color: #bbb;
    border-radius: 10px;
}
.rank h1 {
    text-align: center;
    margin-top: 0px;
    margin-bottom: 0px;
    padding-top :20px;
    padding-bottom :20px;
    background-color: red;
}
.rank-head{
  width: 100%;
  background-color: red;
}
.rank-body{
  width: 100%;
  background-color: blue;
}
.rank-table{
    width: 100%;  
    border-collapse: collapse;  
}
.rank-table tr{
    border-bottom: 1px solid black;
}
.rank-table td{
width: 25%;
text-align: center;
line-height: 50px;
}
</style>