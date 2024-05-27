<template>
    <div v-if="!isLoggedIn">
        <p>Server config admin</p>
        <p>Server: </p>
    </div>

</template>
<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const isLoggedIn = computed(function () {
    return store.getters.getLoggedInState;
});
</script>
<style scoped>

</style>