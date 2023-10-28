<template>
<div class="container-left">
    <div class="topbar">
        <div class="block"><button id="sendRequest0" @click="currentdiv='div1';fetchData(0)">Misc</button><div class="triangle" v-show="currentdiv==='div1'" ></div></div>
        <div class="block"><button id="sendRequest1" @click="currentdiv='div2';fetchData(1)">Crypto</button><div class="triangle" v-show="currentdiv==='div2'" ></div></div>
        <div class="block"><button id="sendRequest2" @click="currentdiv='div3';fetchData(2)">Web</button><div class="triangle" v-show="currentdiv==='div3'" ></div></div>
        <div class="block"><button id="sendRequest3" @click="currentdiv='div4';fetchData(3)">Reverse</button><div class="triangle" v-show="currentdiv==='div4'" ></div></div>
        <div class="block"><button id="sendRequest4" @click="currentdiv='div5';fetchData(4)">Pwn</button><div class="triangle" v-show="currentdiv==='div5'" ></div></div>
    </div>
    <div class="content">
      <div class="Page" v-show="currentdiv==='div1'"><Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div2'"><Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div3'"><Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div4'"><Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div5'"><Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import Question from './Question.vue';
export default {
name:'Showquestion',
components:{Question},
data:function(){
  return{
    currentdiv:'div1',
    retlist:[],
  }
},
methods:{
  fetchData(param) {
      axios.get('http://localhost:80/api/task/list?action=list_all&type='+param+'&is_login=1') // 替换为你的后端API地址  
        .then(response => {  
          // 将后端返回的数据存储在responseData属性中  
          this.retlist = response.data.retlist;  
          console.log(this.retlist);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    },  
  },
  mounted() {  
    // 在页面加载完成后执行函数  
    this.fetchData(0);  
  },  
}
</script>

<style>
.container-left{
  border:1px solid transparent;
  color: #fff;
  float: left;
}
.topbar{
  height: 80px;
  border-bottom: 1px solid transparent;
}
.topbar a{
  width: 200px;
  height: 80px;
  border: 0px;
  font-size: 24px;
  color: #b0b0b0;
  background-color: transparent;
  cursor: pointer;
  text-decoration:none
}
.topbar a:hover{
  color: #fff;
}
.block{
  background-color:#0d1117; 
  position: relative;
  float: left;
  width: 200px;
  height: 80px;
  border-left: 1px solid #2f81f7;
  border-right: 1px solid #2f81f7;
  font-size: 24px;
  text-align: center;
  line-height: 80px;
  border-collapse: collapse;
}
.block button{
  width: 200px;
  height: 80px;
  border: 0px;
  font-size: 24px;
  color: #b0b0b0;
  background-color: transparent;
  cursor: pointer;
}
.content{
  width: 1006.65px;
  background-color:antiquewhite;
  padding-bottom: 30px;
}
/* 点击切换题库内容 */
.triangle{
  width: 0;
  height: 0;
  border-bottom:8px solid #fff ;  
  border-left: 8px solid transparent;  
  border-right:8px solid transparent ;  
  position: absolute;
  top: 80%;
  left: 47%;
} 
.Page{
}
</style>