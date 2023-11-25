<template>
  <div class="message-list">
    <button @click="close()" class="close-btn">&#10006;</button>
    <h2>消息列表</h2>
    <div id="btnSet">
      <button @click="checkMessages()" class="btn">全部标记为已读</button> |
      <button @click="clear()" class="btn1">清空</button>
    </div>
    <br><br>
    <div class="scrollable-container">
      <ul>
      <li v-for="message in messages" :key="message.create_time">
        <div class="message-item">
          <div class="message-origin">{{ message.origin }} :</div>
          <div class="message-text">{{ message.message }}</div>
        </div>
      </li>
    </ul>
    </div>
  </div>
</template>

<script>
import { getMessage, checkMessage } from '../UserSystemApi/MessageApi.js';
import { mapState, mapMutations } from 'vuex';
export default {
  data() {
    return {
      messages: [
        { receiver:"", origin:"", message:"", create_time:'' },
      ],
      num:"",
    };
  },
  computed: {
    ...mapState(['userInfoButtonEnabled','infoBoard','invite','inviteTeam']),
  },
  mounted() {
      this.getMessages();
  },
  methods: {
    ...mapMutations(['setUserInfoButtonEnabled','setInfoBoard','setInvite','setInviteTeam']),
    close() {
      this.setUserInfoButtonEnabled(true);
      this.setInfoBoard(false);
    },
    async getMessages() {
        try {
          const response = await getMessage();
          console.log('获取信息响应', response);
          if(response.ret==='success'){
            this.messages=response.data.message_list;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
    },
    async checkMessages() {
        try {
          const response = await checkMessage();
          console.log('已读信息响应', response);
          if(response.ret==='success'){
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
    },
    clear(){
      this.messages=[];
    },
  },
};
</script>

<style scoped>
.message-list {
  margin-top:-290px;
  margin-left:400px;
  position: absolute;
  width: 500px;
  height: 400px;
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

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

.message-item {
  background-color: grey;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #ccc;
  cursor: pointer;
}

.message-item:hover{
  border-color: red;
}
.message-origin {
  font-weight: bold;
}

.message-text {
  margin-top: 5px;
}

.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
.scrollable-container {
  max-height: 280px; 
  overflow-y: auto; 
}
.btn{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 110px;
    height: 30px;
    border-radius: 5px;
    cursor: pointer;
  }

  .btn1{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 50px;
    height: 30px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn:hover{
    background-color: grey;
  }

  .btn1:hover{
    background-color: grey;
  }

  #btnSet{
    position: absolute;
    right: 20px;
  }
</style>
