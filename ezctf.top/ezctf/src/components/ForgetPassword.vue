<template>
    <div id="ForgetPassword">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1 style="margin-bottom: -5px;">忘记密码</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <br v-if="!err">
      <div>
        <div class="uniquecontainer">
        <label for="newPassword">新密码:</label><br>
        <input type="text" id="newPassword" v-model="newPassword" required /><br><br>
        </div>
        <div class="uniquecontainer">
        <label for="confirmNewPassword">确认新密码:</label><br>
        <input type="text" id="confirmNewPassword" v-model="confirmNewPassword" required /><br><br>
        </div>
        <div class="uniquecontainer">
        <label for="email">邮箱:</label><br>
        <input type="text" id="email" v-model="email" required />
        </div>
        <div class="uniquecontainer">
        <label for="code">验证码:</label><br>
        <input type="text" id="code" v-model="code" /><br><br>
        <button type="submit" @click="Forgetpassword()">发送验证码</button><br><br>
        </div>
        <button class="uniquebutton" @click="reset_password()" :disabled="!btn">完成</button><br><br>
      </div>
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
      isValid(string) {
          const Regex = /^[a-zA-Z0-9_]+$/;
          return (string) => Regex.test(string);
      },
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
            if (!this.isValid(this.newPassword)) {
              this.setErr("密码只能包含数字、字母和下划线");
              return;
            }
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
              this.setLog(true);
              this.setFoPa(false);
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
    position: absolute;
    top: auto;
    left: auto;
    width: 450px;
    height: 490px;
    justify-content: center;
    align-items: center;
    background-color: #1e1e1e;
    padding: 20px;
    border-style: solid;
    border-radius: 20px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
}
.uniquecontainer label{
    float: left;
    margin-left:10px;
    margin-bottom: 2px;
  }
  .uniquecontainer input{
    border-top: transparent;
    border-left: transparent;
    border-right: transparent;
    border-bottom: 2px solid #fff;
    background-color: transparent;
    height: 25px;
    width: 220px;
    font-size: 20px;
    color: #fff;
  }
  .uniquecontainer input:focus{   
    outline: none;
    border-top: transparent;
    border-left: transparent;
    border-right: transparent;
    border-bottom: 2px solid #fff;
    background-color: transparent;
    height: 25px;
    width: 220px;
    font-size: 20px;
    color: #fff;
  }
  .uniquecontainer {  
    width: 250px;
    background-color: #1e1e1e;
    margin: 0 auto;
    margin-bottom:5px;
    border-radius: 5px;
    padding-top: 5px;
  }
  .uniquebutton{
    width: 70px;
    height: 35px;
    font-size: 16px;
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
    padding: 4px;
    color:red;
    font-size: small;
}
</style>