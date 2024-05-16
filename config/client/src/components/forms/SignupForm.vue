<template>
    <div class="config-form-fields">
        <label for="firstName" class="config-form-label">Voornaam</label>
        <input type="text" name="firstName" id="firstName" ref="firstName">
        <label for="lastName" class="config-form-label">Achternaam</label>
        <input type="text" name="lastName" id="lastName" ref="lastName">
        <label for="emailAddress" class="config-form-label">Email Address</label>
        <input type="email" name="emailAddress" id="emailAddress" ref="emailAddress">
        <label for="password" class="config-form-label">Password</label>
        <input type="password" name="password" id="password" ref="password">
        <label for="password1" class="config-form-label">Herhaal password</label>
        <input type="password1" name="password1" id="password1" ref="password1">

    </div>
</template>
<script setup>

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