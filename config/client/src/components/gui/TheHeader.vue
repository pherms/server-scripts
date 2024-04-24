<template>
    <div class="header">
        <h1>Header</h1>
        <submit-button @click="openModal">Login</submit-button>
        <modal-component :isOpen="isModalOpened" @modal-close="closeModal" @modal-submit="submitHandler" name="login-modal">
            <template #content></template>
            <template #footer></template>
        </modal-component>
    </div>
</template>
<script setup>
// import LoginForm from '../forms/LoginForm.vue'
import SubmitButton from '../ui/SubmitButton.vue';
import ModalComponent from './ModalComponent.vue';
import { ref } from "vue";

const isModalOpened = ref(false);
const openModal = () => {
    isModalOpened.value = true;
};

const closeModal = () => {
    isModalOpened.value = false;
};

const submitHandler = () => {
    console.log("login pressed")
    // Do whaterver on submit
};


</script>
<style scoped>

</style>