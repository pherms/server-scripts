<template>
    <h1>Backup Config</h1>
    <backup-configform></backup-configform>
</template>
<script>
import BackupConfigform from '../forms/BackupConfigForm'

export default ({
    setup() {
        
    },
    components: {
        BackupConfigform,
    }
})
</script>
<style scoped>
* {
    color: #1E0342;
}
</style>