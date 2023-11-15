<template>
    <div id="deleteTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>解散战队</h1>
      <input v-model="password" placeholder="请输入密码" /><br><br>
      <button @click="delete_team()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { delete_Team } from '@/UserSystemApi/TeamApi';
  export default {
    data() {
      return {
        password: "",
      };
    },
    computed: {
    ...mapState(['teamname','isLeader','deleteTeam']),
    },
    methods: {
      ...mapMutations(['setTeanmane','setIsLeader','setDeleteTeam']),
      async delete_team() {
        try {
          const response = await delete_Team(this.password);
          console.log('解散战队响应:', response);
          if (response.return === 'success') {
            alert(response.msg);
            this.setTeamname('');
            this.setIsLeader(false);
            document.cookie = "teamname=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
            document.cookie = `isLeader=${false}; path=/`;
            this.setDeleteTeam(false);
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('错误:', error);
          console.log(error.response);
        }
      },
      close() {
        this.setDeleteTeam(false);
      },
    },
  };
</script>
<style>
#deleteTeam {
    margin-top:200px;
    margin-left:670px;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 170px;
    background-color: #1e1e1e;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border-style: solid;
    border-radius: 5px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
    z-index: 10;
}
.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
</style>
 