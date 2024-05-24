<template>
    <div>
        <h1>Backup Sources config</h1>
        <backup-sourcesform></backup-sourcesform>
    </div>
</template>
<script>
import BackupSourcesform from '../forms/BackupSourcesForm.vue'

export default ({
    setup() {
        
    },
    components: {
        BackupSourcesform,
    }
})
</script>

<style scoped>

</style>BackupSourcesForm