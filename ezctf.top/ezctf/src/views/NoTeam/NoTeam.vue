<template>
    <div id="noTeam">
      <router-link to="/Home" class="close-btn">&#10006;</router-link>
      <h1>选择战队</h1>
      <div>
        <router-link to ='/CreateTeam' class="router-link">创建战队</router-link> |
        <router-link to ='/JoinTeam' class="router-link">加入战队</router-link>
      </div>
    </div>
</template>

<script>
    export default {
        props: ['user'], 
    };
</script>

<style>
#noTeam {
    margin-top:200px;
    margin-left:500px;
    position: fixed;
    top: auto;
    left: auto;
    width: 20%;
    height: 15%;
    background-color: black;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border-style: solid;
    border-radius: 5px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
}

.router-link {
    text-decoration: none;
    color: white;
}

.router-link:hover {
    color: blue;
}

.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
</style>
