<template>
    <div v-if="isOpen" class="modal-mask">
        <div class="modal-wrapper">
            <div class="modal-container" ref="target">
                <div class="modal-body">
                    <slot name="content">
                        <login-form v-if="!isSignup"></login-form>
                        <signup-form v-if="isSignup"></signup-form>
                    </slot>
                </div>
                <div class="modal-footer">
                    <div class="modal-buttons">
                        <slot name="footer">
                            <submit-button v-if="!isSignup" @click="emit('modal-submit')">Login</submit-button>
                            <submit-button v-if="isSignup" @click="emit('modal-submitSignup')">Opslaan</submit-button>
                            <submit-button @click.stop="emit('modal-close')">Annuleren</submit-button>
                        </slot>
                    </div>
                    <a href="#" v-if="!isSignup" @click="emit('modal-signup')">Nog geen account? Maak er 1 aan</a>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import LoginForm from '../forms/LoginForm.vue';
import SignupForm from '../forms/SignupForm.vue';
import SubmitButton from '../ui/SubmitButton.vue';
import { ref } from "vue";
import { onClickOutside } from '@vueuse/core';

defineProps({
    isOpen: Boolean,
    isSignup: Boolean
});

const emit = defineEmits(["modal-close","modal-submit","modal-signup","modal-submitSignup"]);

const target = ref(null);
onClickOutside(target, () => emit('modal-close'))


</script>

<style scoped>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
}

.modal-container {
    width: 300px;
    margin: 150px auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.33);
    color: #1E0342;
}

.modal-footer {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: center;
}

.modal-buttons {
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
}
</style>