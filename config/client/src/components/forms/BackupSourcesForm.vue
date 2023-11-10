<template>
    <form action="#" method="post" id="sourcesConfig">
        <label for="sources" class="input-form-label">Sources om te backuppen</label>
        <textarea name="sources" id="sources" cols="30" rows="10" class="config-form-fields input-border config-form-input w-fit"></textarea>
    </form>
    <submit-button></submit-button>
</template>
<script>
import SubmitButton from '../ui/SubmitButton.vue'

export default ({
    setup() {
        
    },
    components: {
        SubmitButton,
    }
})
</script>

<style scoped>
.input-border {
  border-color: rgb(30 41 59/0,8);
  border: solid 1px;
  border-radius: 5px;
  padding: 0.25rem;
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