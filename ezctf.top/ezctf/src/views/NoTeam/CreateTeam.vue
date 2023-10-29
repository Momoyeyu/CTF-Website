<template>
    <div id="createTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>创建战队</h1>
      <form @submit.prevent="createTeam">
        <label for="teamname">战队名称:</label>
        <input type="text" id="teamname" v-model="team.team_name" required /><br><br>
        <label for="check">审核加入:</label>
        <input type="checkbox" id="check" v-model="team.check" /><br><br>
        <button type="submit" @click="createteam()">创建战队</button>
      </form>
    </div>
</template>

<script>
import { createTeam } from '/src/UserSystemApi/TeamApi.js';
 import { mapState, mapMutations } from 'vuex';
 export default {
    data() {
      return {
        team: {
          team_name: '',
          leader_name: this.$store.state.username,
          check: false
        },
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
      async createTeam() {
        try {
          const response = await createTeam(this.team.leader_name, this.team.team_name, !this.team.check);
          alert(response.data.msg);
          console.log('创建战队响应', response);
          setTeamname(this.team.team_name);
        } catch (error) {
          alert(error.response.data.msg);
          console.log('错误：',error);
        }
      }, 
      createteam() {
        this.createTeam();
        this.setUserInfoButtonEnabled(true);
        this.$router.push("/Home");
      }
    },
  };
</script>

<style>
#createTeam {
    margin-top:200px;
    margin-left:500px;
    position: fixed;
    top: auto;
    left: auto;
    width: 350px;
    height: 200px;
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
</style>
  
