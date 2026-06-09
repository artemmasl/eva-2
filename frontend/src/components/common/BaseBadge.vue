<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    variant?: 'neutral' | 'primary' | 'success' | 'sale' | 'info';
    size?: 'sm' | 'md';
  }>(),
  {
    variant: 'neutral',
    size: 'md',
  },
);

const variantClass = computed(() => ({
  neutral: 'bg-surface-control text-text-primary',
  primary: 'bg-primary text-text-inverse',
  info: 'bg-primary/10 text-primary',
  success: 'bg-[#e7f7ee] text-[#1a7f4b]',
  sale: 'bg-accent text-text-inverse',
}[props.variant]));

const sizeClass = computed(() => (props.size === 'sm' ? 'h-5 px-2 text-[11px]' : 'h-6 px-2.5 text-xs'));
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1 rounded-pill font-medium leading-none',
      sizeClass,
      variantClass,
    ]"
  >
    <slot />
  </span>
</template>
