<template>
    <div id="noTeam">
        <button @click="close()" class="close-btn">&#10006;</button>
      <h1>选择战队</h1>
      <div>
        <router-link to ='/CreateTeam' class="router-link">创建战队</router-link> |
        <router-link to ='/JoinTeam' class="router-link">加入战队</router-link>
      </div>
    </div>
</template>

<script>
    import { mapState, mapMutations } from 'vuex';
    export default {
        computed: {
            ...mapState(['userInfoButtonEnabled']),
        },
        methods: {
            ...mapMutations(['setUserInfoButtonEnabled']),
            close() {
                this.setUserInfoButtonEnabled(true);
                this.$router.push('/Home');
            },
        }
    };

</script>

<style>
#noTeam {
    margin-top:220px;
    margin-left:550px;
    position: fixed;
    top: auto;
    left: auto;
    width: 250px;
    height: 120px;
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
