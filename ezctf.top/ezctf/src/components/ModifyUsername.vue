<template>
    <div>
      <input v-model="newUsername" placeholder="请输入新用户名" />
      <button @click="updateUsername">确认</button>
    </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        newUsername: "",
      };
    },
    methods: {
      updateUsername() {
        // 触发自定义事件，将新用户名传递给父组件
        this.$emit("updateUsername", this.newUsername);
        // 清空输入框
        this.newUsername = "";
      },
    },
  };
  </script>
  