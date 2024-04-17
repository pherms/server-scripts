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
<script>
import SideBar from './SideBar.vue';

export default {
    setup() {
        
    },
    components: {
        SideBar
    }

}
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