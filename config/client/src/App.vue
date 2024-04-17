<template>
  <the-header></the-header>
  <main-nav></main-nav>
  <main-content></main-content>
</template>
<script>
import MainNav from './components/nav/MainNav.vue'
import TheHeader from './components/gui/TheHeader.vue'
import MainContent from './components/gui/MainContent.vue'

export default {
  setup() {
    
  },
  components: {
    TheHeader,
    MainNav,
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