<template>
  <div>
    <form @submit.prevent="signupHandler" class="config-form-fields">
      <label for="firstName" class="config-form-label">Voornaam</label>
      <input type="text" v-model="firstName" name="firstName" id="firstName">
      <label for="lastName" class="config-form-label">Achternaam</label>
      <input type="text" v-model="lastName" name="lastName" id="lastName">
      <label for="emailAddress" class="config-form-label">Email Address</label>
      <input type="email" v-model="emailAddress" name="emailAddress" id="emailAddress">
      <label for="password" class="config-form-label">Password</label>
      <input type="password" v-model="password" name="password" id="password">
      <label for="password1" class="config-form-label">Herhaal password</label>
      <input type="password" v-model="password1" name="password1" id="password1">
    </form>
    <div class="form-buttons">
    <submit-button class="form-button" @click="signupHandler">
      <span class="material-symbols-outlined">
          person
      </span>
      Opslaan
    </submit-button>
    <submit-button class="form-button" @click.stop="emit('modal-close')">
        <span class="material-symbols-outlined">
            close_small
        </span>
        Annuleren
    </submit-button>
    </div>
  </div>
</template>
<!-- <script setup>

const firstName = ref('');
const lastName = ref('');
const emailAddress = ref('');
const password = ref('');
const password1 = ref('');
</script> -->
<script setup>
import { ref } from 'vue';
import SubmitButton from "../ui/SubmitButton.vue";
import { useStore } from 'vuex';

const firstName = ref('');
const lastName = ref('');
const emailAddress = ref('');
const password = ref('');
const password1 = ref('');

const emit = defineEmits(["modal-close"]);
const store = useStore()
   
async function signupHandler() {

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
          mode: 'cors',
          headers: { "Content-type": "application/json; charset=UTF-8" },
          // headers: { 'Content-Type': 'x-www-form-urlencoded' },
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
  store.commit('toggleModalState', false);
}
  
</script>
<style scoped>
.input-border {
  border-color: #1E0342;
  border: solid 1px;
  border-radius: 5px;
  padding: 0.4rem;
  line-height: 32px;
  font-size: 18px;
  color: #1E0342;
}

.input-border:focus {
    border-color: #0E46A3;
}

.config-form-fields {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.config-form-label {
  display: inline-block;
  position: relative;
  margin: 0.25rem 0.75rem;
}

.w-fit {
  width: -moz-fit-content;
  width: fit-content;
}

.material-symbols-outlined {
    font-size: 18px;
}

.form-buttons {
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
}

.form-button {
    gap: 0.25rem;
}

.form-footer {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: center;
}
</style>