<script setup lang="ts">
const search = defineModel<string>({ required: true });
</script>

<template>
  <input
    v-model="search"
    class="h-14 rounded-full border px-6 text-base outline-none"
    :class="$style.search"
    type="search"
    placeholder="Search spaces"
  />
</template>

<style module lang="scss">
.search {
  width: min(100%, 680px);
  color: var(--color-text-primary);
  background: var(--color-surface);
  border-color: var(--color-border);
  box-shadow: var(--shadow-floating);

  &:focus {
    border-color: var(--color-primary);
  }
}
</style>
