<template>
    <div id="forgetPassword">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>忘记密码</h1>
      <form @submit.prevent="forgetPassword">
        <label for="email">邮箱:</label>
        <input type="text" id="email" v-model="ForgetPassword.email" required />
        <button type="submit" @click="getVcode()">发送验证码</button><br><br>
        <label for="Vcode">验证码:</label>
        <input type="text" id="Vcode" v-model="Vcode.Vcode" required /><br><br>
        <button @click="next()">下一步</button><br><br>
      </form>
    </div>
</template>
    
<script>
  import { mapState, mapMutations } from 'vuex';
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
      computed: {
      ...mapState(['log','FoPa','RePa']),
      },
      methods: {
        ...mapMutations(['setLog','setFoPa','setRePa']),
        close() {
          this.setFoPa(false);
          this.setLog(true);
        },
        getVcode() {
          // 发送获取验证码请求到后端
        },
        next() {
            //发送验证码，验证是否正确
            this.setRePa(true);
            this.setFoPa(false);
        }
      },
    };
</script>
    
<style>
#forgetPassword {
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