<template>
  <div class="message-list">
    <button @click="close()" class="close-btn">&#10006;</button>
    <h2>消息列表</h2>
    <ul>
      <li v-for="message in messages" :key="message.id">
        <div class="message-item">
          <div class="message-sender">{{ message.sender }}</div>
          <div class="message-text">{{ message.text }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
export default {
  data() {
    return {
      messages: [
        { id: 1, sender: "jwf", text: "欢迎来到ezctf" },
        { id: 2, sender: "yyl", text: "Hello world!" },
        { id: 3, sender: "lwk", text: "sjj" },
        // 添加更多消息...
      ],
    };
  },
  computed: {
    ...mapState(['userInfoButtonEnabled']),
  },
  methods: {
    ...mapMutations(['setUserInfoButtonEnabled']),
    close() {
      this.setUserInfoButtonEnabled(true);
      this.$router.push('/Home');
    },
  },
};
</script>

<style scoped>
.message-list {
  margin-top:100px;
  margin-left:450px;
  position: fixed;
  top: auto;
  left: auto;
  width: 30%;
  height: 45%;
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
  border: 1px solid #ccc;
}

.message-sender {
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
</style>
