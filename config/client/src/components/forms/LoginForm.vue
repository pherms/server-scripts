<template>
    <div class="config-form-fields">
        <label for="emailAddress" class="config-form-label w-fit">Email:</label>
        <input type="email" name="emailAddress" id="emailAddress" ref="emailAddress">
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" ref="password">
    </div>
    <submit-button @click="submitData">Login</submit-button>
    <h5 id="accessToken" ref="accessToken">{{ accessToken }}</h5>
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
        submitData() {
            console.log('Submit login button press');
            const enteredEmailAddress = this.$refs.emailAddress.value;
            const enteredPassword = this.$refs.password.value;

            console.log('Entered emailadres: ' + enteredEmailAddress);
            console.log('Entered password: ' + enteredPassword);

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emailAddress: enteredEmailAddress, password: enteredPassword })
            };
            fetch('http://127.0.0.1:8081/api/v1/auth', requestOptions)
                .then(async response => {
                    const isJson = response.headers.get('content-type')?.includes('application/json');
                    const data = isJson && await response.json();

                    // check for error response
                    if (!response.ok) {
                        const error = (data && data.message) || response.status;
                        return Promise.reject(error);
                    }

                    // console.log(data.accessToken);
                    this.$refs.accessToken = data.accessToken;
                })
                .catch(error => {
                    console.error("Er is iets fout gegaan!", error);
                });
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

.config-form-fields {
  display: flex;
  justify-content: space-between;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  padding-left: 1rem;
}

.config-form-label {
  position: relative;
}

.w-fit {
  width: -moz-fit-content;
  width: fit-content;
}
</style>