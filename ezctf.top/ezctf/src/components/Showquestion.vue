<template>
<div class="container-left">
    <div class="topbar">
        <div class="block"><button class="blockbutton active" @click="TotalChange(0)">
          Misc</button><div class="triangle" v-show="currentdiv==='div1'" ></div></div>
        <div class="block"><button class="blockbutton" @click="TotalChange(1)">
          Crypto</button><div class="triangle" v-show="currentdiv==='div2'" ></div></div>
        <div class="block"><button class="blockbutton" @click="TotalChange(2)">
          Web</button><div class="triangle" v-show="currentdiv==='div3'" ></div></div>
        <div class="block"><button class="blockbutton" @click="TotalChange(3)">
          Reverse</button><div class="triangle" v-show="currentdiv==='div4'" ></div></div>
        <div class="block"><button class="blockbutton" @click="TotalChange(4)">
          Pwn</button><div class="triangle" v-show="currentdiv==='div5'" ></div></div>
    </div>
    <div class="content1">
      <div class="Page" v-show="currentdiv==='div1'">
        <Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div2'">
        <Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div3'">
        <Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div4'">
        <Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
      <div class="Page" v-show="currentdiv==='div5'">
        <Question v-for="item in retlist" :key="item.task_id" :item="item"/></div>
    </div>    
</div>
</template>
<script>
import axios from 'axios';
import Question from './Question.vue';
import { mapState } from 'vuex';
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
      axios.get('http://localhost:80/api/task/query?action=list&type='+param) // 替换为你的后端API地址  
        .then(response => {  
          this.retlist = response.data.data.task_list;  
          console.log(this.retlist);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    },
    TotalChange(param){
      if(this.isLogin){
      this.changediv(param);
      this.changeCSS(param);}
      else{      
        alert("前面的区域登录以后再来探索吧~~");
        this.$router.push("/Log");}
    },
    changediv(param)
    {
      this.currentdiv='div'+(param+1);
      this.fetchData(param);
    },
    changeCSS(){  
      for(let i=0;i<5;i++){
    let buttons = document.getElementsByClassName('blockbutton');  
    buttons[i].onclick=function(){
    for (let j = 0; j < buttons.length; j++) {  
      if (buttons[j] == this) {  
        buttons[j].classList.add('active');  
      } else {  
        buttons[j].classList.remove('active');  
      }  
      }}}
    },
  },
  computed:{
    ...mapState(['isLogin']),
},
  mounted() {  
    // 在页面加载完成后执行函数  
    this.changediv(0);  
    this.changeCSS();  
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
  color: #7d8590;
  background-color: transparent;
  cursor: pointer;
  text-decoration:none
}
.topbar a:hover{
  color: #fff;
}
.block{
  background-color:#161b22; 
  position: relative;
  float: left;
  width: 200px;
  height: 80px;
  font-size: 24px;
  text-align: center;
  line-height: 80px;
  border-radius: 3px;
}
.blockbutton{
  width: 200px;
  height: 80px;
  border: 0px;
  font-size: 24px;
  color: #c0c0c0;
  background-color: transparent;
  transition: color 0.3s ease; 
  transition: background-color 0.3s ease; 
  cursor: pointer;
  border-radius: 5px;
}
.blockbutton:hover {  
  color: #ffffff;
  background-color: #1f6feb;  
}
.active{
  color: #ffffff;
  background-color: #1f6feb;  
}
.content1{
  width: 1000px;
  background-color:#0d1117;
  padding-bottom: 30px;
  border-top: 1px solid #5b5959;
  border-bottom: 2px solid #5b5959;
  overflow: hidden;
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
</style>