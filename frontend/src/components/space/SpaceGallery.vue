<template>
  <section>
    <img v-for="image in images" :key="image" :src="image" alt="Space image" />
  </section>
</template>
<script setup lang="ts">
defineProps<{
  images: string[];
}>();
</script>
