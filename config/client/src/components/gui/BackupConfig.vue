<template>
    <div v-if="isLoggedIn">
        <h1>Backup Config</h1>
        <backup-configform></backup-configform>
    </div>
</template>
<script setup>
import BackupConfigform from '../forms/BackupConfigForm'
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const isLoggedIn = computed(function () {
    return store.getters.getLoggedInState;
});

</script>
<style scoped>
* {
    color: #1E0342;
}
</style>