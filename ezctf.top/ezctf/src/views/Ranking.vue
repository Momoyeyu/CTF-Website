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
                <td>{{ item.name }}</td>
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
export default {
name:'Ranking',
data(){
    return{
        users: [  
        {  
          name: "张三",  score: 85,  last_commit: 114514 , 
        },  
        {  
          name: "李四",  score: 90,  last_commit: 114514 , 
        },  
        {  
          name: "王五",  score: 10,  last_commit: 114514 ,
        } 
      ],
      teams: [  
        {  
            team_id: 0, team_name: "JDG", member_count: 5, score:80,
        },  
        {  
            team_id: 1, team_name: "BLG", member_count: 5, score:90, 
        },  
        {  
            team_id: 2, team_name: "LNG", member_count: 5, score:85 ,
        },
        {  
            team_id: 3, team_name: "WBG", member_count: 5, score:95,
        },
      ]  
    }
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