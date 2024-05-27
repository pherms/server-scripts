<template>
    <div class="sidebar">
        <div class="top-icons">
            <router-link v-if="isLoggedIn" to="/backupConfig">
                <div class="button">
                    <span class="material-symbols-outlined">
                        settings
                    </span>
                </div>
            </router-link>
            <router-link v-if="isLoggedIn" to="/backupSources">
                <div class="button">
                    <span class="material-symbols-outlined">
                        add_task
                    </span>
                </div>
            </router-link>
        </div>
    
        <div class="bottom-icons">
            <div class="button" v-if="isLoggedIn">
            <span class="material-symbols-outlined">
                account_circle
            </span>
            </div>
        </div>
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
.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 300,
  'GRAD' 0,
  'opsz' 32
}

.sidebar {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 90vh;
    width: 4rem;
    background-color: #0E46A3;
    color: #E1F7F5;
    padding: 0.25rem;
    text-decoration: none;
}

.button {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    height: 2.5rem;
    margin-top: 0.5rem;
    width: 3.5rem;
    border-radius: 8px;
    transition: 0.3s;
}

.button:visited {
    text-decoration: none;
}

a:visited {
    color: #E1F7F5;
}

.button:hover {
    background: #9AC8CD;
    color: #1E0342;
    font-size: 40px
}

.bottom-icons {
    margin-bottom: 0.5rem;
}
</style>