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
        <i v-else class="iconfont icon-weiwancheng"></i>
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
      axios.get('http://localhost:80/api/task/query?action=detail&task_id='+param) // 替换为你的后端API地址  
        .then(response => {  
          // 将后端返回的数据存储在responseData属性中  
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
  color:#61cd61;
} 
.question{
  margin-left:38px;
  margin-top:30px;
  border: 1px solid #2f81f7;
  width: 438px;
  height: 180px;
  display: inline-block;
}
.question button{
  border: 0px;
  padding: 0px;
  cursor: pointer;
}
.question-left{
float: left;
width: 300px;
height: 180px;
border-right: 1px solid red;
}
.question-name{
  width: 300px;
  height: 91px;
  border-bottom: 1px solid red;
  text-align: center;
  line-height: 90px;
  /* padding-left: 16px; */
  color: #272e3b;
  font-size: 24px;
  font-weight: 600;
  text-shadow: 0px 6px 13px rgba(0,0,0,.1);
}
.question-source{
  width: 300px;
  height: 44px;
  border-bottom: 1px solid red;
  text-align: center;
  line-height: 44px;
  /* padding-left: 16px; */
  color: #6b7784;
}
.question-message{
  width: 300px;
  height: 43px;
  border-bottom: 1px solid transparent;
  color: #242e3b;
}
.question-score{
  float: left;
  width: 149px;
  /* height:44px; */
  border-right: 1px solid red;
  text-align: center;
  line-height: 44px;
  /* padding-left: 16px; */
}
.question-amount{
  float: left;
  width: 150px;
  /* height:44px; */
  text-align: center;
  line-height: 44px;
  /* padding-left: 16px; */
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
.popup-wrap{
  position: fixed;  
  top: 0;  
  left: 0;  
  width: 100%;  
  height: 100%;  
  background-color: rgba(0, 0, 0, 0.7);  
  z-index: 9999; 
}
.popup{
  width: 700px;
  padding: 10px;
  position: absolute;  
  top: 50%;  
  left: 50%;  
  transform: translate(-50%, -50%);  
  background-color: #bbb;  
  border-radius: 5px;  
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
.popup-header{
  width: 700px;
  height: 30px;
  padding-top: 10px;
  padding-bottom: 10px;
  background-color: #fff;
  text-align: center;
  position: relative;
}
.popup-content{
  color: #000;
  width: 652px;
  height: 400px;
  padding: 24px;
  background-color: #fff;
}
.TITLE{
  color: #000;
  font-size: 24px;
  font-weight: bold;
  float: left;
  margin-left: 20px;
}
.close{
  float: right;
  height: 24px;
  border: 0 solid transparent;
  background:transparent;
  color: #000;
  cursor: pointer;
  margin-right: 10px;
  padding: 2px;
  font-size: 26px;             
  /* border-radius: 50%; */
}
.close:hover{
  color: blue;
}
.describe{
  width: 100%;
}
.popup-table {  
  width: 100%;  
  border-collapse: collapse;  
} 
.popup-table td {  
  padding: 20px;
  border-bottom: 1px solid #ccc;
} 
.popup-flag{
  text-align: center;  
  margin-top: 150px; 
}
.popup-flag input{
  border: 1px solid #000;
  width:200px;
  height: 30px;
  border-radius: 5px;
}
.popup-download {  
  text-align: center;  
  margin-top: 10px;  
} 
</style>