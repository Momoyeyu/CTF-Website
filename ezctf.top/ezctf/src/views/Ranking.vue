<template>
<div class="rank">
  <div class="user-rank">
    <div class="rank-head">
    <h1>用户排行榜</h1>
    </div>
    <div class="rank-body">
        <table class="rank-table">
            <tr v-if="this.isLogin" class="Myrank-title">
                <td>我的排名</td>
                <td>姓名</td>
                <td>得分</td>
                <td>上次提交</td>
            </tr>
            <tr v-if="this.isLogin" class="Myrank-body">
              <!-- 在模板或者计算属性中尝试访问一个对象的 'rank' 属性，但是那个对象在那个时刻是未定义的。 -->
                <td>#{{ fetchMy[0].rank }}</td>
                <td>{{ fetchMy[0].username }}</td>
                <td>{{ fetchMy[0].score}}</td>
                <td>{{ fetchMy[0].last_commit }}</td>
            </tr>
            <tr class="table-title">
                <td>总排名</td>
                <td>姓名</td>
                <td>得分</td>
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
          <tr v-if="this.isLeader||this.isMember" class="Myrank-title">
                <td>我的排名</td>
                <td>姓名</td>
                <td>得分</td>
                <td>上次提交</td>
            </tr>
            <tr v-if="this.isLeader||this.isMember" class="Myrank-body">
              <!-- 在模板或者计算属性中尝试访问一个对象的 'rank' 属性，但是那个对象在那个时刻是未定义的。 -->
                <td>#{{ fetchMyteam[0].rank }}</td>
                <td>{{ fetchMyteam[0].team_name }}</td>
                <td>{{ fetchMyteam[0].member_count}}</td>
                <td>{{ fetchMyteam[0].score }}</td>
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
      axios.get('http://localhost:80/api/rank/user') 
        .then(response => {  
          this.users = response.data.data.user_list;  
          console.log(this.users);
          console.log(this.fetchMy);
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
    } ,
    fetchMy() {  
      // 根据用户信息查询用户得分排名等排行榜信息，假设你已经有了一个名为this.username的状态来保存用户的用户名  
      return this.sortedUsers.filter(obj => obj.username === this.username);   
    },  
    fetchMyteam() {  
      // 根据团队名称查询团队得分排名等排行榜信息，假设你已经有了一个名为this.teamname的状态来保存团队的名称  
      return Myteam = this.sortedTeams.filter(obj => obj.team_name === this.teamname);   
    }, 
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