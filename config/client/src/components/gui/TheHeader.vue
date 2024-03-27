<template>
    <div class="header">
        <h1>Header</h1>
        <div class="loginform">
            <login-form></login-form>
        </div>
    </div>
</template>
<script>
import LoginForm from '../forms/LoginForm.vue'

export default {
    setup() {
        
    },
    components: {
        LoginForm
    }
}
</script>
<style scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}
</style>