<template>
  <div>
    <div class="config-form-fields">
      <label for="emailAddress" class="config-form-label w-fit">Login/Email:</label>
      <input type="email" name="emailAddress" id="emailAddress" ref="emailAddress">
      <label for="password" class="config-form-label">Password:</label>
      <input type="password" name="password" id="password" ref="password">
    </div>
    <div class="formbutton">
      <submit-button @click="submitData">Login</submit-button>
      <h5 id="accessToken" ref="accessToken">{{ accessToken }}</h5>
    </div>
  </div>
</template>
<script>
import SubmitButton from '../ui/SubmitButton.vue'

export default {
    setup() {

    },
    components: {
        SubmitButton
    },
    methods: {
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
        async submitData() {
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
        }
    }
}
</script>
<style scoped>
.input-border {
  border-color: rgb(30 41 59/0,8);
  border: solid 1px;
  border-radius: 5px;
  padding: 0.25rem;
}
.config-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.25rem;
}

.config-form-col2 {
  grid-column-start: 2;
}

.config-form-input {
  position: relative;
  width: 20rem;
}

.formbutton {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 0.75rem;
}
.config-form-fields {
  display: flex;
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
</style>