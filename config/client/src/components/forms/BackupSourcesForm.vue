<template>
  <div class="layout">
    <form action="#" method="post" id="sourcesConfig">
        <label for="sources" class="input-form-label">Sources om te backuppen</label>
        <textarea name="sources" id="sources" cols="30" rows="10" class="config-form-fields input-border config-form-input w-fit"></textarea>
    </form>
    <submit-button>Opslaan</submit-button>
  </div>
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
  border-color: #1E0342;
  border: solid 1px;
  border-radius: 5px;
  padding: 0.4rem;
}

.config-form-input {
  line-height: 32px;
  font-size: 18px;
  color: #1E0342;
  margin: 1rem 1rem;
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
  margin-bottom: 1rem;
}

.w-fit {
  width: -moz-fit-content;
  width: fit-content;
}

.layout {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>