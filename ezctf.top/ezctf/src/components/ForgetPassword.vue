<template>
    <div id="ForgetPassword">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>忘记密码</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <form @submit.prevent="reset_password">
        <label for="newPassword">新密码:</label>
        <input type="text" id="newPassword" v-model="newPassword" required /><br><br>
        <label for="confirmNewPassword">确认新密码:</label>
        <input type="text" id="confirmNewPassword" v-model="confirmNewPassword" required /><br><br>
        <label for="email">邮箱:</label>
        <input type="text" id="email" v-model="email" required />
        <button type="submit" @click="Forgetpassword()">发送验证码</button><br><br>
        <label for="code">验证码:</label>
        <input type="text" id="code" v-model="code" /><br><br>
        <button type="submit" :disabled="!btn">完成</button><br><br>
      </form>
    </div>
</template>
    
<script>
  import { mapState, mapMutations } from 'vuex';
  import { forgetPassword, resetPassword } from '../UserSystemApi/UserApi.js';
    export default {
      data() {
        return {
          newPassword:"",
          confirmNewPassword:"",
          email: '',
          code:'',
          btn: false,
        };
      },
      computed: {
      ...mapState(['log','FoPa','err','loginButtonEnabled']),
      },
      methods: {
        ...mapMutations(['setLog','setFoPa','setErr','setLoginButtonEnabled']),
        close() {
          this.setFoPa(false);
          this.setLog(true);
          this.setErr("");
        },
        async forget_password() {
          try {
            const response = await forgetPassword(this.email);
            alert(response.msg);
            console.log('修改密码响应:', response);
            if (response.ret === 'success') {
              this.btn=true;
              this.setErr("");
            }
          } catch (error) {
            this.setErr(error.response.data.msg);
            console.error('修改密码错误:', error);
          }
        },
        Forgetpassword(){
          if(this.newPassword==this.confirmNewPassword&&this.newPassword!=''){
              console.log(this.newPassword);
              console.log(this.confirmNewPassword);
              this.forget_password();
          }
          else{
              this.newPassword='';
              this.confirmNewPassword='';
              this.setErr("密码设置失败，请重新设置密码！");
          } 
        },
        async reset_password() {
          try {
            const response = await resetPassword(this.code,this.email,this.newPassword);
            alert(response.msg);
            console.log('修改密码响应:', response);
            if (response.ret === 'success') {
              this.btn=false;
              this.setErr("");
              this.$router.push('/');
              this.setLoginButtonEnabled(true);
            }
          } catch (error) {
            this.setErr(error.response.data.msg);
            console.error('修改密码错误:', error);
          }
        },
      },
    };
</script>
    
<style>
#ForgetPassword {
    margin-top:150px;
    margin-left:480px;
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
#er{
    height: 8px;
    color:red;
    font-size: small;
}
</style>