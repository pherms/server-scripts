<template>
    <button type="submit" class="button">Submit</button>
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
  background-color: blue;
  color: white;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  width: 6rem;
}

.button:hover,
input[type=submit]:hover {
  text-shadow: 0 0 5px white;
  cursor: pointer;
}
</style>