<template>
    <div class="sidebar">
        <div class="top-icons">
            <router-link to="/backupConfig">
                <div class="button">
                    <span class="material-symbols-outlined">
                        settings
                    </span>
                </div>
            </router-link>
            <router-link to="/backupSources">
                <div class="button">
                    <span class="material-symbols-outlined">
                        add_task
                    </span>
                </div>
            </router-link>
        </div>
    
        <div class="bottom-icons">
            <div class="button">
            <span class="material-symbols-outlined">
                account_circle
            </span>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    setup() {

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

@keyframes iconsize {
    0% {
        font-size: 24px;
        background-color: #1E0342;
    }
    100% {
        font-size: 32px;
        background-color: #0E46A3;
    }
}

.sidebar {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100vh;
    width: 4rem;
    background-color: #1E0342;
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

.button:hover {
    background: #0E46A3;
    font-size: 40px
    /* animation-name: iconsize;
    animation-duration: 0.2s; */
}

.bottom-icons {
    margin-bottom: 0.5rem;
}
</style>