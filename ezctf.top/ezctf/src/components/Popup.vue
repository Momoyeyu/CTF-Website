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
                  <td v-if="item.solved">状态：已完成</td>  
                  <td v-else>状态：未完成</td>  
                </tr>  
              </table>  
              <p class="popup-description">题目描述：{{ Detail.content }}</p>
              <p v-if="item.solved" class="popup-flag"></p>
            <div v-else class="popup-flag">  
              <input type="text" v-model="inputData" placeholder="请输入FLAG~~"/>  
              <button @click="checkInput">提交</button> 
              </div> 
            <div class="popup-download">  
                <a :href="downloadLink" @click="handleDownloadClick">点击下载附件</a>  
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
    inputData: "",
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
    else this.isModalVisible = !this.isModalVisible;

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
      axios.post('http://localhost:80/api/task/answer?action=commit_flag',this.Flag)  
        .then(response=>{  
          console.log(response.data);  //答题成功立刻修改（未完成）
          if (response.data.msg==="CORRECT"){
            alert("回答正确！！！")
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
        const response = await axios.get('http://localhost:80/api/task/answer?action=download_attachment&task_id='+this.item.task_id, 
        { responseType: 'blob' }); // 发送下载请求，并指定响应类型
        this.downloadLink = window.URL.createObjectURL(response.data); // 创建下载链接  
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