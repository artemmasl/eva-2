<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    size?: 'sm' | 'md' | 'lg';
    variant?: 'surface' | 'ghost' | 'primary';
    active?: boolean;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
  }>(),
  {
    size: 'md',
    variant: 'surface',
    active: false,
    disabled: false,
    type: 'button',
  },
);

const sizeClass = computed(() => ({
  sm: 'h-8 w-8',
  md: 'h-9 w-9',
  lg: 'h-11 w-11',
}[props.size]));

const toneClass = computed(() => {
  if (props.active) {
    return 'bg-primary text-text-inverse hover:bg-primary-hover';
  }

  return {
    surface: 'bg-surface-control text-text-primary hover:bg-border',
    ghost: 'bg-transparent text-text-secondary hover:bg-surface-control',
    primary: 'bg-primary text-text-inverse hover:bg-primary-hover',
  }[props.variant];
});
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'grid cursor-pointer place-items-center rounded-full border-0 transition-colors',
      sizeClass,
      toneClass,
      disabled && 'cursor-not-allowed opacity-60',
    ]"
  >
    <slot />
  </button>
</template>
