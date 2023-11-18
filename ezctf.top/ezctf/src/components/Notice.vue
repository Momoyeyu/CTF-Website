<template>
<div class="container-right">
    <div class="outline">Latest News</div>
    <div class="notice">
        <ul>
            <li>1.THis</li>
            <li>2.is</li>
            <li>3.my</li>
            <li>4.first</li>
            <li>5.Web</li>
        </ul>
    </div>
</div>
</template>

<script>
export default {
name:'Notice'
}
</script>

<style>
.container-right{
  width: 200px;
  border:1px solid #2f81f7;
  color: #fff;
  float: right;
}
.outline{
  text-align: center;
  height: 60px;
  border-bottom: 1px solid #2f81f7;
  font-size: 18px;
  line-height: 60px;
  letter-spacing: 0.1em;
}
.notice ul{
  list-style: none;
  padding-left: 10px;
  line-height: 40px;
}
</style>