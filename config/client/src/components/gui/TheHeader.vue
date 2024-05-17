<template>
    <div class="header">
        <div class="title">
            <div class="exo-2-title-400">Server</div>
            <div class="handlee-regular-200">Config</div>
        </div>
        <submit-button class="header-button" @click="openModal">
            <div class="button-icon">
                <span class="material-symbols-outlined">
                login
                </span>
            </div>
            <div class="button-text">
                Login
            </div>
        </submit-button>
        <!-- <modal-component :isOpen="isModalOpened" :isSignup="isSignupOpened" @modal-close="closeModal" @modal-submit="submitHandler" @modal-signup="openSignupForm" @modal-submitSignup="signupHandler" name="login-modal"> -->
        <modal-component :isOpen="isModalOpened" :isSignup="isSignupOpened" @modal-close="closeModal" @modal-submit="submitHandler" @modal-signup="openSignupForm" name="login-modal">
            <template #content></template>
            <template #footer></template>
        </modal-component>
        
    </div>
</template>
<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

import SubmitButton from '../ui/SubmitButton.vue';
import ModalComponent from './ModalComponent.vue';

const store = useStore();
// const isModalOpened = ref(false);
// const isSignupOpened = ref(false);

const isModalOpened = computed(function () {
    return store.getters.getModalState;
});

const isSignupOpened = computed(function () {
    return store.getters.getSignupFormState;
})

// verwijderen ivm gebruik store
// const openModal = () => {
//     // isModalOpened.value = true;
//     store.commit('toggleModalState', true);
// };
function openModal() {
    store.commit('toggleModalState', true);
}

// verwijderen ivm gebruik store
// const closeModal = () => {
//     // isModalOpened.value = false;
//     store.commit('toggleModalState', false);
//     isSignupOpened.value = false;
// };

function closeModal() {
    store.commit('toggleModalState', false);
}

const openSignupForm = () => {
    console.log("Signup pressed")
    isSignupOpened.value = true;
};

const submitHandler = async() => {
    console.log("login pressed")
    
    try {
        const enteredEmailAddress = this.$refs.emailAddress.value;
        const enteredPassword = this.$refs.password.value;

        console.log('Entered emailadres: ' + enteredEmailAddress);
        console.log('Entered password: ' + enteredPassword);

        const requestOptions = {
            method: 'POST',
            // headers: { 'Content-Type': 'application/json' },
            headers: { 'Content-Type': 'x-www-form-urlencoded' },
            body: new URLSearchParams({
            'emailAddress': enteredEmailAddress,
            'password': enteredPassword
            }).toString()
            // JSON.stringify({ emailAddress: enteredEmailAddress, password: enteredPassword })
        };

        const response = await fetch('http://127.0.0.1:8081/api/v1/auth', requestOptions);
        if (!response.ok) {
            console.log("Error");
        }

    } catch (error) {
            console.error("Er is iets fout gegaan!!", error);
    }
    // Do whaterver on submit
};



// return { isModalOpened, isSignupOpened, openModal, closeModal, openSignupForm, submitHandler, signupHandler };

</script>
<!-- <script setup>
// import LoginForm from '../forms/LoginForm.vue'
import SubmitButton from '../ui/SubmitButton.vue';
import ModalComponent from './ModalComponent.vue';
import { ref } from "vue";

const isModalOpened = ref(false);
const isSignupOpened = ref(false);

const openModal = () => {
    isModalOpened.value = true;
};

const closeModal = () => {
    isModalOpened.value = false;
    isSignupOpened.value = false;

};

const openSignupForm = () => {
    console.log("Signup pressed")
    isSignupOpened.value = true;
};

const submitHandler = async() => {
    console.log("login pressed")
    
    try {
        const enteredEmailAddress = this.$refs.emailAddress.value;
        const enteredPassword = this.$refs.password.value;

        console.log('Entered emailadres: ' + enteredEmailAddress);
        console.log('Entered password: ' + enteredPassword);

        const requestOptions = {
            method: 'POST',
            // headers: { 'Content-Type': 'application/json' },
            headers: { 'Content-Type': 'x-www-form-urlencoded' },
            body: new URLSearchParams({
            'emailAddress': enteredEmailAddress,
            'password': enteredPassword
            }).toString()
            // JSON.stringify({ emailAddress: enteredEmailAddress, password: enteredPassword })
        };

        const response = await fetch('http://127.0.0.1:8081/api/v1/auth', requestOptions);
        if (!response.ok) {
            console.log("Error");
        }

    } catch (error) {
            console.error("Er is iets fout gegaan!!", error);
    }
    // Do whaterver on submit
};

const signupHandler = async() => {
    const firstName = ref('');
    const lastName = ref('');
    const emailAddress = ref('');
    const password = ref('');
    const password1 = ref('');
    console.log("Opslaan pressed")
    try {
        const enteredPassword = password.value;
        const verifyEnteredPassword = password1.value;

        if (enteredPassword !== verifyEnteredPassword) {
            console.log("Passwords do not match");
            return;
        }

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'x-www-form-urlencoded' },
            body: JSON.stringify({firstName: firstName.value, lastName: lastName.value, emailAddress: emailAddress.value, password: enteredPassword})
        };
        console.log(requestOptions)

        const response = await fetch('http://127.0.0.1:8081/api/v1/users', requestOptions);
        if (!response.ok) {
            console.log("Error");
        }
        
    } catch (error) {
        console.error("Er is iets fout gegaan!", error);
    }
    // isSignupOpened.value = true;
};


</script> -->
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100..900;1,100..900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100..900;1,100..900&family=Handlee&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

/* <uniquifier>: Use a unique and descriptive class name
<weight>: Use a value from 100 to 900 */
/* * {
    outline: limegreen 1px solid;
} */
.exo-2-title-400 {
  font-family: "Exo 2", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
  font-size: 3.5rem;
  position: relative;
}

.handlee-regular-200 {
  font-family: "Handlee", cursive;
  font-weight: 200;
  font-style: normal;
  font-size: 1.5rem;
  color:#9AC8CD;
  text-align:right;
  position: absolute;
  left: 146px;
  top: 80px;
}

.title {
    display: flex;
    padding: 1rem;
    flex-direction: column;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1E0342;
    color: #E1F7F5;
    padding: 0.25rem 1.5rem;
}

.header-button {
    background: #0E46A3;
    color: #E1F7F5;
    display: inline-flex;
    justify-content: center;
    gap: 0.5rem;
    align-items: center;
    height: 2.5rem;
    margin-top: 0.5rem;
    border-radius: 8px;
    transition: 0.3s;
    padding: 0.75rem 1rem;
}

.header-button:visited {
    text-decoration: none;
}

a:visited {
    color: #E1F7F5;
}

.header-button:hover {
    background: #9AC8CD;
    color: #1E0342;
    font-size: 14px;
    
    /* animation-name: iconsize;
    animation-duration: 0.2s; */
}

.material-symbols-outlined {
    font-size: 18px;
}
</style>