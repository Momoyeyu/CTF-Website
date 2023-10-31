<template>
    <div id="resetPassword">
      <router-link to="/Log" class="close-btn">&#10006;</router-link>
      <h1>重置密码</h1>
      <form @submit.prevent="Complete">
        <label for="newPassword">新密码:</label>
        <input type="text" id="newPassword" v-model="ResetPassword.newPassword" required /><br><br>
        <label for="confirmNewPassword">确认新密码:</label>
        <input type="text" id="confirmNewPassword" v-model="ResetPassword.confirmNewPassword" required /><br><br>
        <button type="submit">完成</button><br><br>
      </form>
    </div>
</template>
    
<script>
    export default {
      data() {
        return {
          ResetPassword: {
            newPassword: '',
            confirmNewPassword: '',
          },
        };
      },
      methods: {
        resetpassword() {
          // 发送重置密码请求到后端
        },
        Complete() {
            if(this.ResetPassword.newPassword==this.ResetPassword.confirmNewPassword&&this.ResetPassword.newPassword!=''){
              this.resetpassword();
              this.$router.push("/Log");
            }
            else{
                this.ResetPassword.newPassword='';
                this.ResetPassword.confirmNewPassword='';
                alert("密码设置失败，请重新设置密码！");
            } 
        },
      },
    };
</script>
    
<style>
#resetPassword {
    margin-top:200px;
    margin-left:480px;
    position: absolute;
    top: auto;
    left: auto;
    width: 450px;
    height: 220px;
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