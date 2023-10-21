<template>
<div id="question" class="question"><button id="trigger" class="trigger" onclick="showpopup()">
    <div class="question-left">
        <div id="question-name" class="question-name"></div>
        <div id="question-source" class="question-source">来源：</div>
        <div class="question-message">
            <div id="question-score" class="question-score">分数：</div>
            <div id="question-amount" class="question-amount">解出人数：</div>
        </div>
    </div>
    <div class="question-right">
        <i class="iconfont">&#xe817;</i></div>
</button></div>
</template>

<script>
export default {
name:'Question'
}
</script>

<style>
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
</style>