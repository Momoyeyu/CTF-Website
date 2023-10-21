<template>
<div>
<Banner/>
<div class="wrap">
<Showquestion/>
<Notice/>
</div>
</div>
</template>

<script>
import Banner from '../components/Banner.vue';
import Showquestion from '../components/Showquestion.vue';
import Notice from '../components/Notice.vue';
export default {
name:'Ranking',
components:{Banner,Showquestion,Notice}
}
</script>

<style>
.wrap{
  width: 1300px;
  margin: 0 auto;
}
</style>