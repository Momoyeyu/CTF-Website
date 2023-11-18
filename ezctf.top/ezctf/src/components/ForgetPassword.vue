<template>
    <div id="forgetPassword">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>忘记密码</h1>
      <form @submit.prevent="forgetPassword">
        <label for="newPassword">新密码:</label>
        <input type="text" id="newPassword" v-model="newPassword" required /><br><br>
        <label for="confirmNewPassword">确认新密码:</label>
        <input type="text" id="confirmNewPassword" v-model="confirmNewPassword" required /><br><br>
        <label for="email">邮箱:</label>
        <input type="text" id="email" v-model="email" required />
        <button type="submit" @click="getVcode()">发送验证码</button><br><br>
        <label for="code">验证码:</label>
        <input type="text" id="code" v-model="code" required /><br><br>
        <button @click="next()">完成</button><br><br>
      </form>
    </div>
</template>
    
<script>
  import { mapState, mapMutations } from 'vuex';
    export default {
      data() {
        return {
          newPassword:"",
          confirmNewPassword:"",
          email: '',
          code:'',
        };
      },
      computed: {
      ...mapState(['log','FoPa','RePa']),
      },
      methods: {
        ...mapMutations(['setLog','setFoPa','setRePa']),
        close() {
          this.setFoPa(false);
          this.setLog(true);
        },
      },
    };
</script>
    
<style>
#forgetPassword {
    position: absolute;
    top: auto;
    left: auto;
    width: 450px;
    height: 300px;
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
</style>