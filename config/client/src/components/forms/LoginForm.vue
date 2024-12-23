<template>
  <div>
    <div class="config-form-fields">
      <label for="emailAddress" class="config-form-label w-fit">Login/Email:</label>
      <input type="email" @input="clearError" v-model="emailAddress" name="emailAddress" id="emailAddress">
      <label for="password" class="config-form-label">Password:</label>
      <input type="password" @input="clearError" v-model="password" name="password" id="password">
    </div>
    <div class="error" v-if="isError">{{ errorMessage }}</div>
    <div class="form-buttons">
      <submit-button class="modal-button" @click="loginUser">
          <span class="material-symbols-outlined">
              login
          </span>
          Login
      </submit-button>

      <submit-button class="modal-button" @click="closeLoginForm">
          <span class="material-symbols-outlined">
              close_small
          </span>
          Annuleren
      </submit-button>
    </div>
  </div>
</template>
<script setup>
import { useStore } from 'vuex';
import { ref, computed } from 'vue';
import SubmitButton from '../ui/SubmitButton.vue';
import axios from 'axios';

const store = useStore();
const emailAddress = ref('');
const password = ref('');
const errorMessage = ref('');
// export default {

const isError = computed(function () {
  return store.getters.getErrorState
})
    
function closeLoginForm() {
  store.commit('toggleModalState', false)
}

function clearError() {
  store.commit('toggleErrorState', false)
}

async function loginUser() {
  try {
    const enteredEmailAddress = emailAddress.value;
    const enteredPassword = password.value;

    console.log('Entered emailadres: ' + enteredEmailAddress);
    console.log('Entered password: ' + enteredPassword);

    const url = 'http://' + process.env.VUE_APP_apiserver + '/api/v1/auth';

    const response = await axios.post(url, {
        emailAddress: enteredEmailAddress,
        password: enteredPassword
      }, {
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      },
    });


    console.log(response.status)
    if (response.status === 201 || response.status === 200) {
      console.log(response)
      var accessToken = response.data.accesstoken;
      var username = response.data.User.username;
      var email = response.data.User.emailaddress;

      store.commit('updateAuthToken', accessToken);
      store.commit('updateUserState', {username, email});
      store.commit('toggleLoginState', true);
      store.commit('toggleModalState', false);
    }

    
  } catch (error) {
    // if (error.status === 400) {
    //   store.commit('toggleErrorState', true);
    //   errorMessage.value = 'Ongeldige gebruikersnaam of onjuist paswoord';
    // } else {
      console.error("Er is iets fout gegaan!!", error);
    // }
  }
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

.error {
  margin-top: 0.5rem;
  color: red;
}
</style>