<template>
    <div>
        <side-bar>
            <span></span>
        </side-bar>
        <router-view/>
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
.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 300,
  'GRAD' 0,
  'opsz' 32
}
</style>