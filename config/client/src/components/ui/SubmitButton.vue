<template>
    <button type="submit" class="button"><slot></slot></button>
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
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  width: 6rem;
  height: 2.5rem;
  transition-duration: 300ms;
}

.button:hover,
input[type=submit]:hover {
  background-color: #0E46A3;
  cursor: pointer;
}
</style>