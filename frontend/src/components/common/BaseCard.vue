<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    padding?: 'none' | 'sm' | 'md' | 'lg';
    interactive?: boolean;
  }>(),
  {
    padding: 'md',
    interactive: false,
  },
);

const paddingClass = computed(() => ({
  none: 'p-0',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
}[props.padding]));
</script>

<template>
  <div
    :class="[
      'rounded-card border border-border bg-surface shadow-card',
      paddingClass,
      interactive && 'cursor-pointer transition-[transform,box-shadow] duration-300 ease-out hover:-translate-y-1 hover:shadow-floating',
    ]"
  >
    <slot />
  </div>
</template>
