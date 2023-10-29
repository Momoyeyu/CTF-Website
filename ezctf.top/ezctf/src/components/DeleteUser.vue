<template>
    <div id="deleteUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>账户注销</h1>
      <input v-model="password" placeholder="请输入密码" /><br><br>
      <button @click="deleteUser()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { deleteUserInfo } from '@/UserSystemApi/UserApi';
  export default {
    data() {
      return {
        username:this.$store.state.username,
        password: "",
      };
    },
    computed: {
    ...mapState(['username','modifyUser','deleteUser','isLogin']),
    },
    methods: {
      ...mapMutations(['setUsername','setModifyUser','setDeleteUser','setIsLogin']),
      async deleteUser() {
        try {
          const response = await deleteUserInfo(this.username, this.password);
          console.log('注销账户响应:', response);
          if (response.return === 'success') {
            alert(response.data.msg);
            this.$store.commit('isLogin', false);
            this.$store.commit('deleteUser', false);
          }
        } catch (error) {
          alert('错误!');
          console.error('错误:', error);
          console.log(error.response);
        }
      },
      close() {
        this.setDeleteUser(false);
      },
    },
  };
</script>
<style>
#deleteUser {
    margin-top:-220px;
    margin-left:500px;
    position: fixed;
    top: auto;
    left: auto;
    width: 250px;
    height: 170px;
    background-color: black;
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
 