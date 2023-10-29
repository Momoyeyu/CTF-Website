<template>
<div>
<Banner/>
<div class="wrap">
<Showquestion/>
<Notice/>
<ModifyUser v-if="modifyUser"/>
<DeleteUser v-if="deleteUser"/>
<InfoBoard v-if="infoBoard"/>
</div>
</div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import Banner from '../components/Banner.vue';
import Showquestion from '../components/Showquestion.vue';
import Notice from '../components/Notice.vue';
import ModifyUser from '../components/ModifyUser.vue';
import DeleteUser from '../components/DeleteUser.vue';
import InfoBoard from '../components/InfoBoard.vue';
export default {
name:'Ranking',
components:{Banner,Showquestion,Notice,ModifyUser,DeleteUser,InfoBoard},
computed: {
    ...mapState(['modifyUser','deleteUser','infoBoard']),
},
methods: {
  ...mapMutations(['setModifyUser','setDeleteUser','setInfoBoard']),
}
}
</script>

<style>
.wrap{
  width: 1300px;
  margin: 0 auto;
}
</style>