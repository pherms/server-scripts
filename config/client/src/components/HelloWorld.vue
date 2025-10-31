<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
        <p>
        Welcome to your Vue.js + Vite app.
        </p>
        <p>
        For a guide and recipes on how to configure / customize this project,<br>
        check out the
        <a href="https://vitejs.dev/guide/" target="_blank" rel="noopener">Vite documentation</a>.<br>
        Also check the
        <a href="https://vuejs.org/guide/introduction.html" target="_blank" rel="noopener">Vue.js documentation</a>.
        </p>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const msg = ref('new message')
</script>
<style scoped>
h1, h2 {
  font-weight: normal;
}
</style>