<template>
<div class="question"><button :id="item.task_id" class="trigger" @click="showpopup();fetchData(item.task_id)">
    <div class="question-left">
        <div id="question-name" class="question-name">{{ item.task_name }}</div>
        <div id="question-source" class="question-source">{{ item.src }}</div>
        <div class="question-message">
            <div id="question-score" class="question-score">分数：{{ item.points }}</div>
            <div id="question-amount" class="question-amount">解出人数：{{ item.solve_count }}</div>
        </div>
    </div>
    <div class="question-right">
        <i v-if="item.solved" class="iconfont icon-yiwancheng" :class="['iconfont-green']"></i>
        <i v-else class="iconfont icon-weiwancheng" :class="['iconfont-white']"></i>
      </div>
</button>
<Popup :item="item" :Detail="Detail" ref="Popup"/>
</div>
</template>

<script>
import axios from 'axios'
import Popup from './Popup.vue'
export default {
name:'Question',
components:{ Popup },
props:{
    item:{
      type:Object,
      required: true,
    }
  },
data:function(){
  return{
    isModalVisible: false,
    Detail:{},
  }
},
methods:{
  showpopup() {  
    this.$refs.Popup.showpopup();
},
fetchData(param) {
      axios.get('/api/task/query?action=detail&task_id='+param) // 替换为你的后端API地址  
        .then(response => {  
          this.Detail = response.data.data;  
          console.log(this.Detail);
        })  
        .catch(error => {  
          console.error(error);  
        });  
    },  
}
}
</script>

<style>
.iconfont-green {  
  color:#238636;
} 
.iconfont-white {  
  color:#fff;
} 
.question{
  margin-left:38px;
  margin-top:30px;
  border: 1px solid #5b5959;
  width: 438px;
  height: 180px;
  display: inline-block;
  background-color: #161b22;
  border-radius: 15px;
  padding: 5px;
}
.question button{
  border: 0px;
  padding: 0px;
  cursor: pointer;
  background-color:transparent;
}
.question-left{
float: left;
width: 300px;
height: 180px;
border-right: 1px solid #5b5959;
}
.question-name{
  width: 300px;
  height: 91px;
  border-bottom: 1px solid #5b5959;
  text-align: center;
  line-height: 90px;
  color: #fff;
  font-size: 24px;
  font-weight: 600;
  text-shadow: 0px 6px 13px rgba(0,0,0,.1);
}
.question-source{
  width: 300px;
  height: 44px;
  border-bottom: 1px solid #5b5959;
  text-align: center;
  line-height: 44px;
  color: #aaa;
}
.question-message{
  width: 300px;
  height: 43px;
  border-bottom: 1px solid transparent;
  color: #fff;
}
.question-score{
  float: left;
  width: 149px;
  border-right: 1px solid #5b5959;
  text-align: center;
  line-height: 44px;
}
.question-amount{
  float: left;
  width: 150px;
  text-align: center;
  line-height: 44px;
}
.question-right{
float:right;
width: 137px;
height: 180px;
text-align: center;
line-height: 180px;
}
.question-right .iconfont{
  font-family: "iconfont" !important;
  font-size: 80px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>