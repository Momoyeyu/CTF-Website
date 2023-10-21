<template>
<div class="popup-wrap" id="popup-wrap" onclick="hidepopup()">
    <div class="popup">
        <div class="popup-header">
            <div class="TITLE">TITLE</div>
            <button class="close" onclick="hidepopup()">X</button>
        </div>
        <div class="popup-content">
            <table class="popup-table">  
                <tr>  
                  <td>来源：</td>  
                  <td>分数：</td>  
                </tr>  
                <tr>  
                  <td>解出人数：</td>  
                  <td>状态：</td>  
                </tr>  
              </table>  
              <p class="popup-description">
                题目描述：
            </p>
            <!-- <div class="popup-flag">  
              <input type="text" class="inputText" placeholder="请输入FLAG" /> 
              </div>  -->
              <!-- 点击关闭bug -->
            <div class="popup-download">  
                <a href="#" download>附件点击这里下载</a>  
              </div>  
        </div>
    </div>
</div>
</template>

<script>
export default {
name:'Popup',
methods:{
    showpopup() {  
  var popup = document.getElementById("popup-wrap");  
  popup.style.display = "block";  
},
    hidepopup() {  
  var popup = document.getElementById("popup-wrap");  
  popup.style.display = "none";  
}
}
}
</script>

<style>
.popup-wrap{
  display: none;  
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
  height: 28px;
  border: 0 solid transparent;
  background: #888;
  color: #fff;
  cursor: pointer;
  margin-right: 10px;
  font-size: 20px;             
  /* border-radius: 50%; */
}
.close:hover{
  background: #888;
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
/* .popup-flag{
} */
.popup-download {  
  text-align: center;  
  margin-top: 100px;  
} 
</style>