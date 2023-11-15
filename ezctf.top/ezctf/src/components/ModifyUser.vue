<template>
    <div id="modifyUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>修改信息</h1>
      <input v-model="newUsername" placeholder="请输入新用户名" /><br><br>
      <input v-model="password" placeholder="请输入密码" /><br><br>
      <button @click="modify_User()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { modifyUserInfo } from '@/UserSystemApi/UserApi';
  export default {
    data() {
      return {
        user_name:this.$store.state.username,
        newUsername: "",
        password: "",
      };
    },
    computed: {
    ...mapState(['username','teamname','modifyUser']),
    },
    methods: {
      ...mapMutations(['setUsername','setTeamname','setModifyUser']),
      async modify_User() {
        try {
          const response = await modifyUserInfo(this.user_name, this.newUsername,this.password);
          console.log('修改信息响应:', response);
          if (response.ret === 'success') {
            alert(response.msg);
            this.setModifyUser(false);
            this.setUsername(response.data.new_username);
            sessionStorage.setItem('username', response.data.new_username)
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('错误:', error);
        }
      },
      close() {
        this.setModifyUser(false);
      },
    },
  };
</script>
<style>
#modifyUser {
    margin-top:-180px;
    margin-left:500px;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 200px;
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
 