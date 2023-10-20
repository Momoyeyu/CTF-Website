<template>
    <div id="forgetPassword">
      <router-link to="/Log" class="close-btn">&#10006;</router-link>
      <h1>忘记密码</h1>
      <form @submit.prevent="forgetPassword">
        <label for="email">邮箱:</label>
        <input type="text" id="email" v-model="ForgetPassword.email" required />
        <button type="submit" @click="getVcode()">发送验证码</button><br><br>
        <label for="Vcode">验证码:</label>
        <input type="text" id="Vcode" v-model="Vcode.Vcode" required /><br><br>
        <button type="submit" @click="next()">下一步</button><br><br>
      </form>
    </div>
</template>
    
<script>
    export default {
      data() {
        return {
          ForgetPassword: {
            email: '',
          },
          Vcode: {
            Vcode:'',
          },
        };
      },
      methods: {
        getVcode() {
          // 发送获取验证码请求到后端
        },
        next() {
            //发送验证码，验证是否正确
            this.$router.push("/Reset");
        }
      },
    };
</script>
    
<style>
#forgetPassword {
    margin-top:150px;
    margin-left:450px;
    position: fixed;
    top: auto;
    left: auto;
    width: 30%;
    height: 25%;
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