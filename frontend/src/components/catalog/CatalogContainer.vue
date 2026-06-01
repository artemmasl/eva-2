<script setup lang="ts">
import PageScroll from '@/components/common/PageScroll.vue';
</script>

<template>
  <div class="flex h-screen flex-col overflow-hidden px-6 pb-7 max-md:px-3 max-md:pb-4" :class="$style.container">
    <slot name="header" />
    <slot name="top" />
    <PageScroll class="flex-auto">
      <slot />
    </PageScroll>
    <slot name="footer" />
    <slot name="overlay" />
  </div>
</template>

<style module lang="scss">
.container {
  padding-top: 120px;
  color: var(--color-text-primary);
  background: var(--color-surface-muted);
}
</style>
