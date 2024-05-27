<template>
    <div v-if="isLoggedIn">
        <h1>Backup Sources config</h1>
        <backup-sourcesform></backup-sourcesform>
    </div>
</template>
<script setup>
import BackupSourcesform from '../forms/BackupSourcesForm.vue'

import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const isLoggedIn = computed(function () {
    return store.getters.getLoggedInState;
})

</script>

<style scoped>

</style>