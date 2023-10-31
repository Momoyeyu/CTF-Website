<template>
    <div id="bkg">
        <Login v-if="log"/>
        <Registration v-if="reg"/>
        <ForgetPassword v-if="FoPa"/>
        <ResetPassword v-if="RePa"/>
    </div>
</template>
<script>
import { mapState, mapMutations } from 'vuex';
import Registration from '@/components/Registration.vue';
import Login from '@/components/Login.vue';
import ForgetPassword from '@/components/ForgetPassword.vue';
import ResetPassword from '@/components/ResetPassword.vue';
export default {
    components: { Registration,Login,ForgetPassword,ResetPassword },
    computed: {
    ...mapState(['log','reg','FoPa','RePa']),
    },
    methods: {
    ...mapMutations(['setLog','setReg','setFoPa','setRePa']),
    }
}
</script>
    
<style>
#bkg{
  background-color:#1e1e1e;
}
</style>