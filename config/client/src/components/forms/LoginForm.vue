<template>
  <div>
    <div class="config-form-fields">
      <label for="emailAddress" class="config-form-label w-fit">Login/Email:</label>
      <input type="email" v-model="emailAddress" name="emailAddress" id="emailAddress">
      <label for="password" class="config-form-label">Password:</label>
      <input type="password" v-model="password" name="password" id="password">
    </div>
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
import { ref } from 'vue';
import SubmitButton from '../ui/SubmitButton.vue';
import axios from 'axios';

const store = useStore();
const emailAddress = ref('');
const password = ref('');
// export default {
    
function closeLoginForm() {
  store.commit('toggleModalState', false)
}

async function loginUser() {
  try {
    const enteredEmailAddress = emailAddress.value;
    const enteredPassword = password.value;

    console.log('Entered emailadres: ' + enteredEmailAddress);
    console.log('Entered password: ' + enteredPassword);

    // const requestOptions = {
    //   method: 'POST',
    //   headers: { "Content-type": "application/json; charset=UTF-8" },
    //   // headers: { 'Content-Type': 'x-www-form-urlencoded' },
    //   // body: new URLSearchParams({
    //   //   'emailAddress': enteredEmailAddress,
    //   //   'password': enteredPassword
    //   // }).toString()
    //   body: JSON.stringify({ emailAddress: enteredEmailAddress, password: enteredPassword })
    // };

    // const response = await fetch('http://127.0.0.1:8081/api/v1/auth', requestOptions);
    const response = await axios.post('http://127.0.0.1:8081/api/v1/auth', {
        emailAddress: enteredEmailAddress,
        password: enteredPassword
      }, {
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      },
    });

    if (response.status === 201) {
      console.log(response.data.accessToken);
      console.log(response.data.user.name);
      console.log(response.data.user.emailAddress);
      store.commit('updateAuthToken', response.data.accessToken);
      store.commit('updateUserState', response.data.user);
      store.commit('toggleLoginState', true);
      store.commit('toggleModalState', false);
    }

    
  } catch (error) {
    console.error("Er is iets fout gegaan!!", error);
  }
}
    
    // },
    // components: {
        
    // },
    // methods: {
        // submitData() {
        //     console.log('Submit login button press');
        //     const enteredEmailAddress = this.$refs.emailAddress.value;
        //     const enteredPassword = this.$refs.password.value;

        //     console.log('Entered emailadres: ' + enteredEmailAddress);
        //     console.log('Entered password: ' + enteredPassword);

        //     const requestOptions = {
        //         method: 'POST',
        //         // headers: { 'Content-Type': 'application/json' },
        //         headers: { 'Content-Type': 'x-www-form-urlencoded' },
        //         body: JSON.stringify({ emailAddress: enteredEmailAddress, password: enteredPassword })
        //     };
        //     fetch('http://127.0.0.1:8081/api/v1/auth', requestOptions)
        //         .then(async response => {
        //             const isJson = response.headers.get('content-type')?.includes('application/json');
        //             const data = isJson && await response.json();

        //             // check for error response
        //             if (!response.ok) {
        //                 const error = (data && data.message) || response.status;
        //                 return Promise.reject(error);
        //             }

        //             // console.log(data.accessToken);
        //             // this.$refs.accessToken = data.accessToken;
        //         })
        //         .catch(error => {
        //             console.error("Er is iets fout gegaan!", error);
        //         });
        // }
        // async submitData() {
        //   try {
        //     const enteredEmailAddress = this.$refs.emailAddress.value;
        //     const enteredPassword = this.$refs.password.value;

        //     console.log('Entered emailadres: ' + enteredEmailAddress);
        //     console.log('Entered password: ' + enteredPassword);

        //     const requestOptions = {
        //       method: 'POST',
        //       // headers: { 'Content-Type': 'application/json' },
        //       headers: { 'Content-Type': 'x-www-form-urlencoded' },
        //       body: new URLSearchParams({
        //         'emailAddress': enteredEmailAddress,
        //         'password': enteredPassword
        //       }).toString()
        //       // JSON.stringify({ emailAddress: enteredEmailAddress, password: enteredPassword })
        //     };

        //     const response = await fetch('http://127.0.0.1:8081/api/v1/auth', requestOptions);
        //     if (!response.ok) {
        //       console.log("Error");
        //     }

        //   } catch (error) {
        //     console.error("Er is iets fout gegaan!!", error);
        //   }
        // }
//     }
// }
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

</style>