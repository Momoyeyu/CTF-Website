<template>
  <div>
      <Navigation/>
      <router-view/>
  </div>
  </template>
  <script>
  import Navigation from './components/Navigation.vue'
  export default {
    components: { Navigation },
    name:'App'
  }
  </script>
  
  <style>
  body{
    background-color: #010409;
  }
  </style>
  