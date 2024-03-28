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
                  <td>难度：{{ item.difficulty }}</td>  
                  <td v-if="item.solved">状态：已完成</td>  
                  <td v-else>状态：未完成</td>  
                </tr>  
              </table>  
              <div class="huadong"><p class="popup-description">题目描述：{{ Detail.content }}</p></div>
              <p v-if="item.solved"></p>
            <div v-else class="popup-flag">  
              <div>
                <button v-if="(item.task_type===2||item.task_type===4)&&!this.iscountdown" 
                class="onlineStage" @click="GetonlineStage(item.task_id)">
                <i class="iconfont icon-diannao"></i>创建在线场景</button>
              <div v-if="this.iscountdown">
                <a :href="ipandport" style="text-decoration: none;">{{ ipandport }}</a><br>
                <span style="font-size: 14px;">倒计时:{{countdown}}s</span>
                <button class="onlineStage" @click="DeleteonlineStage(item.task_id)">删除场景</button>
              </div>
              </div>
              <input type="text" v-model="inputData" placeholder="请输入FLAG~~"/>  
              <button class="hangin" @click="checkInput">提交</button> 
            </div> 
            <div class="popup-download">  
                <a v-if="Detail.annex" :href="downloadLink" @click="handleDownloadClick">
                  <i class="iconfont icon-xiazai"></i>点击下载附件</a>  
              </div>  
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
export default {
name:'Popup',
data:function(){
  return{
    isModalVisible: false,
    iscountdown:false,
    countdown:0,
    inputData: "",
    ipandport: "",
    Flag:{
      "action": "commit_flag",
      "data": {
        "task_id" :this.item.task_id,
        "flag" : this.inputData,
      }
    },
    downloadLink:"",
    fileDownloadName:"附件.rar",
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
    ...mapState(['isLogin']),
},
methods:{
  showpopup() {  
    if (!this.isLogin)
    {
      alert("前面的区域登录以后再来探索吧~~");
      this.$router.push("/Log");
    }
    else {
      this.isModalVisible = !this.isModalVisible;
      let storedCountdown = localStorage.getItem("countdown"+this.item.task_id); // 从 LocalStorage 中获取倒计时时间  
    if (storedCountdown) { 
      if(!this.intervalId){
      this.countdown = parseInt(storedCountdown); // 将字符串转换为整数，并赋值给倒计时时间变量  
      this.ipandport=localStorage.getItem("ipandport"+this.item.task_id);
      if (this.countdown > 0) {  
        this.iscountdown = true; // 设置倒计时状态为活跃状态（如果倒计时时间大于0）
        this.intervalId = setInterval(() => {  // 定义并赋值给 this.intervalId  
          this.countdown--;    
          if (this.countdown <= 0) {    
          this.DeleteonlineStage();    
          }  
          }, 1000);
      } else {  
        this.iscountdown = false; // 如果倒计时时间为0或负数，则设置倒计时状态为非活跃状态（已停止）  
        localStorage.removeItem('countdown');
        this.DeleteonlineStage(this.item.task_id);   
      }}
    } else {  
      // 如果 LocalStorage 中不存在倒计时时间，则默认为非活跃状态（已停止）或根据需要进行其他处理  
    } 
    }

},
  hidepopup() {  
  this.isModalVisible = false; 
},
checkInput() {  
      // 检查输入是否为空，如果不为空则提交数据  
      if (this.inputData.trim() !== "") {          
        this.Flag.data.flag=this.inputData;
        this.submitData();  

      } else {  
        alert("请输入有效的数据！"); 
      }  
    }, 
    submitData() {  
      console.log(this.Flag);
      axios.post('/api/task/answer?action=commit_flag',this.Flag)  
        .then(response=>{  
          console.log(response.data);
          if (response.data.data.correct){
            alert("回答正确！！！")
            window.location.reload();  
          }
          else{
            alert("很可惜回答错误...")
          }
        })  
        .catch(function (error) {  
          console.log(error);  
        });  
        this.inputData= "";
    },
    async getDownloadLink() {    
      try {    
        const response = await axios.get('/api/task/answer?action=download_attachment&task_id='+this.item.task_id,   
        { responseType: 'blob' }); // 发送下载请求，并指定响应类型  
        if (response) {  // 判断响应是否存在  
          this.downloadLink = window.URL.createObjectURL(response.data); // 创建下载链接    
        } else {  
          console.error('下载链接获取失败：响应不存在');  
        }  
      } catch (error) {    
        console.error('下载链接获取失败：', error);    
      }  
    },
    handleDownloadClick(event) {  
      event.preventDefault();
      if (this.downloadLink) {  
        const link = document.createElement('a');  
        link.href = this.downloadLink;  
        link.setAttribute('download', this.fileDownloadName);  
        document.body.appendChild(link);  
        link.click();  
        document.body.removeChild(link);  
      } else {  
        alert('下载链接不存在！');  
      }  
    },
    GetonlineStage() {  
      axios.get('/api/task/answer?action=create_online&task_id='+this.item.task_id) // 替换为你的后端API地址    
        .then(response => {     
          console.log(response.data);    
          if(response.data.ret==="success"){
          this.ipandport=response.data.data.ip+response.data.data.port;
          this.Waitonline();   
          this.countdown = 7200;   
          this.iscountdown = true;   
          this.intervalId = setInterval(() => {  // 定义并赋值给 this.intervalId  
          this.countdown--;    
          if (this.countdown <= 0) {    
          this.DeleteonlineStage();    
          }  
          }, 1000);}
        })    
        .catch(error => {    
          console.error(error);    
        });              
    },      
    Waitonline(){
      axios.get('/api/task/answer?action=wait_online&task_id='+this.item.task_id) // 替换为你的后端API地址    
        .then(response => {    
          console.log(response.data);    
        })    
        .catch(error => {    
          console.error(error);    
        });  
    },
    DeleteonlineStage() {  
      clearInterval(this.intervalId); // 清除由 GetonlineStage 创建的定时器    
      localStorage.removeItem('countdown'+this.item.task_id);
      localStorage.removeItem("ipandport"+this.item.task_id); 
      this.iscountdown = false;   
      axios.get('/api/task/answer?action=stop_online&task_id='+this.item.task_id) // 替换为你的后端API地址    
        .then(response => {    
          console.log(response.data);     
        })    
        .catch(error => {    
          console.error(error);    
        });    
    }, 
  },
  beforeDestroy() {  
    if (this.iscountdown) {  
      localStorage.setItem("countdown"+this.item.task_id, this.countdown); // 将倒计时时间保存到 LocalStorage  
      localStorage.setItem("ipandport"+this.item.task_id, this.ipandport); 
    } else {  
      localStorage.removeItem("countdown"+this.item.task_id); // 如果倒计时已停止，则从 LocalStorage 中移除该项  
      localStorage.removeItem("ipandport"+this.item.task_id); 
    }  
  }, 
  mounted() {  
    this.getDownloadLink(); // 在组件挂载后获取下载链接
  },
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
  padding: 5px;
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
  color: #fff;
  background-color:#1f6feb ;
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
   /* 题目描述太长容易超出容器（未解决） */
  text-align: center;  
  margin-top: 50px; 
}
.popup-flag input{
  border: 1px solid #000;
  width:200px;
  height: 30px;
  border-radius: 5px;
}
.onlineStage{
  width: 100px;
  color: #1f6feb;
}
.onlineStage:hover{
  text-decoration: underline;
}
.hangin{
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
.huadong{
  max-height: 150px;
  overflow-y:auto ;
}
</style>