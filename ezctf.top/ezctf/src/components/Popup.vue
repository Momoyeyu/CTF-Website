<template>
<div class="popup-wrap" id="popup-wrap" v-if="isModalVisible" @click="hidepopup()">
    <div @click.stop class="popup">
        <div class="popup-header">
            <div class="TITLE">{{ Detail.task_name }}</div>
            <button class="close" @click="hidepopup()">X</button>
        </div>
        <div class="popup-content">
            <table class="popup-table">  
                <tr>  
                  <td>来源：{{ item.src }}</td>  
                  <td>分数：{{ item.points }}</td>  
                </tr>  
                <tr>  
                  <td>解出人数：{{ item.solve_count }}</td>  
                  <td v-if="item.is_solved">状态：已完成</td>  
                  <td v-else>状态：未完成</td>  
                </tr>  
              </table>  
              <p class="popup-description">题目描述：{{ Detail.content }}</p>
            <div class="popup-flag">  
              <input type="text" v-model="inputValue" placeholder="请输入FLAG~~">  
              <button @click="submitData">提交</button> 
              </div> 
            <div class="popup-download">  
                <a :href="downloadUrl">附件点击这里下载</a>  
              </div>  
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
export default {
name:'Popup',
data:function(){
  return{
    isModalVisible: false,
    inputValue: '' ,
  }
},
props: {  
    item: {  
      type: Object,
      required: true  
    },
    Detail: {  
      type: Object,
      required: true  
    }
  },
  computed:{
    downloadUrl() {  
      return axios.get('http://localhost:80/api/task/answer?action=download_attachment&task_id=1')
      .then(response =>{
        console.log(response);
      })
      .catch(error => {  
          console.error(error);  
        });  
  },
},
methods:{
  showpopup() {  
    this.isModalVisible = !this.isModalVisible;
},
  hidepopup() {  
  this.isModalVisible = false; 
},
submitData() {  
      axios.post('/api/data', {  value: this.inputValue   })  
      .then(response => {  
        console.log(response);  
      })  
      .catch(error => {  
        console.error(error);  
      });  
      this.inputValue = ''; // 清空输入框  
    }  
  }  
}
</script>

<style>
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
.popup-flag button{
  width: 60px;
  height: 40px;
  border-radius: 5px;
  margin-left: 5px;
  font-size: 16px;
}
.popup-download {  
  text-align: center;  
  margin-top: 10px;  
} 
</style>