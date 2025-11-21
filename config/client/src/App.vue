<template>
  <the-header></the-header>
  <main-content></main-content>
</template>
<script>
import { provide } from 'vue'
import TheHeader from './components/gui/TheHeader.vue'
import MainContent from './components/gui/MainContent.vue'

export default {
  setup() {
    const apiServer = window.APP_CONFIG?.apiServer || process.env.VUE_APP_apiserver || 'default'
    provide('apiServer', apiServer) // now the value is used and available to children
    return {}
  },
  components: {
    TheHeader,
    MainContent
  }
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
