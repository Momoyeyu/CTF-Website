<template>
<div class="container-left">
    <div class="topbar">
        <div class="block current"><a id="sendRequest0" href="#">Misc</a><div class="triangle current"></div></div>
        <div class="block"><a id="sendRequest1" href="#">Crypto</a><div class="triangle"></div></div>
        <div class="block"><a id="sendRequest2" href="#">Web</a><div class="triangle"></div></div>
        <div class="block"><a id="sendRequest3" href="#">Reverse</a><div class="triangle"></div></div>
        <div class="block"><a id="sendRequest4" href="#" >Pwn</a><div class="triangle"></div></div>
    </div>
    <div class="content">
        <router-view/>
    </div>
</div>
</template>

<script>
export default {
name:'Showquestion',
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
}
/* .block button{
  width: 200px;
  height: 80px;
  border: 0px;
  font-size: 24px;
  color: #b0b0b0;
  background-color: transparent;
  cursor: pointer;
} */
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
  display: none;
} 
.page{
  display: none;
}
.topbar .current{
  display: block;
}
.content .current{
  display: block;
}
</style>