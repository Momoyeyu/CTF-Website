<template>
    <div id="createTeam">
      <router-link to="/Home" class="close-btn">&#10006;</router-link>
      <h1>创建战队</h1>
      <form @submit.prevent="createTeam">
        <label for="teamname">战队名称:</label>
        <input type="text" id="teamname" v-model="team.teamname" required /><br><br>
        <label for="check">审核加入:</label>
        <input type="checkbox" id="check" v-model="team.check" /><br><br>
        <button type="submit" @click="createteam()">创建战队</button>
      </form>
      <p>{{ team.leader_id }}</p>
    </div>
</template>

<script>
 export default {
    props: ['leaderId'],
    data() {
      return {
        team: {
          teamname: '',
          leader_id: this.leaderId,
          check: false
        },
      };
    },
    methods: {
      async createTeam() {
        try {
          const response = await createTeam(this.team.leader_id, this.team.teamname, !this.team.check);
          console.log('创建战队响应', response);
        } catch (error) {
          console.log('错误：',error);
        }
      }, 
      createteam() {
        this.createTeam();
        this.$router.push("/Home");
      }
    },
  };
</script>

<style>
#createTeam {
    margin-top:150px;
    margin-left:450px;
    position: fixed;
    top: auto;
    left: auto;
    width: 30%;
    height: 30%;
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
  
