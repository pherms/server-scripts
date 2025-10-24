<template>
    <div v-if="isLoggedIn">
        <div class="header">
            <h1>Backup Config</h1>
        </div>
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

.header {
    display: flex;
    justify-content: left;
    margin-bottom: 0.5rem;
}
</style>