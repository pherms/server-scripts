<template>
    <div class="main">
        <side-bar>
            <span></span>
        </side-bar>
        <div class="configpages">
            <router-view></router-view>
        </div>
    </div>
</template>
<script setup>
import SideBar from './SideBar.vue';


</script>
<style scoped>
.main {
    display: flex;
    gap: 4rem;
}

.configpages {
    justify-content: center;
}
</style>