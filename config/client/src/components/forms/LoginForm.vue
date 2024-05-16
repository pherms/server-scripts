<template>
  <div>
    <div class="config-form-fields">
      <label for="emailAddress" class="config-form-label w-fit">Login/Email:</label>
      <input type="email" name="emailAddress" id="emailAddress" ref="emailAddress">
      <label for="password" class="config-form-label">Password:</label>
      <input type="password" name="password" id="password" ref="password">
    </div>
  </div>
</template>
<script>


export default {
    setup() {

    },
    components: {
        
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
</style>