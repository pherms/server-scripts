<template>
    <div v-if="isLoggedIn">
        <div class="header">
            <h1>Log Viewer</h1>
        </div>
        <log-viewform></log-viewform>
    </div>
</template>

<script setup>
import LogViewform from '../forms/LogViewForm.vue';

import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const isLoggedIn = computed(function () {
    return store.getters.getLoggedInState;
})

</script>

<style scoped>
.header {
    display: flex;
    justify-content: left;
    margin-bottom: 0.5rem;
}
</style>