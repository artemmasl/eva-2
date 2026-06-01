<script setup lang="ts">
const submit = () => {
  window.alert('Contact request placeholder');
};
</script>

<template>
  <form @submit.prevent="submit">
    <input type="text" placeholder="Name" />
    <input type="tel" placeholder="Phone" />
    <button type="submit">Contact manager</button>
  </form>
</template>
