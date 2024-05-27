<template>
    <button type="button" class="button"><slot></slot></button>
</template>
<script>
export default {
  setup() {
      
  },
}
</script>
<style scoped>
.button,
input[type=submit] {
  border: none;
  border-radius: 8px;
  background-color: #1E0342;
  color: #E1F7F5;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  width: 6.75rem;
  height: 2.5rem;
  transition-duration: 300ms;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.button:hover,
input[type=submit]:hover {
  background-color: #0E46A3;
  cursor: pointer;
}
</style>