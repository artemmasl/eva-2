<template>
  <button
    :type="type"
    :class="[
      'inline-flex cursor-pointer items-center justify-center rounded-full border-0 font-normal leading-none transition-colors',
      size === 'xs' && 'min-h-[18px] px-2.5 text-[10px]',
      size === 'sm' && 'h-[22px] px-3 text-[11px]',
      size === 'md' && 'h-[34px] px-4 text-[13px]',
      size === 'lg' && 'h-[48px] px-8 text-base',
      variant === 'circle' && size === 'sm' && 'w-[22px] px-0',
      variant === 'circle' && size === 'md' && 'w-[34px] px-0',
      active
        ? 'bg-primary text-text-inverse hover:bg-primary-hover'
        : tone === 'clear'
          ? 'bg-transparent text-text-primary hover:bg-surface-control'
          : tone === 'white'
            ? 'bg-surface text-text-primary hover:bg-surface-control'
            : tone === 'outline'
              ? 'border border-border bg-transparent text-text-primary hover:border-primary/40'
              : tone === 'muted'
                ? 'bg-[#d9dce5] text-text-primary hover:bg-[#cdd1dd]'
                : 'bg-surface-control text-text-primary hover:bg-border',
    ]"
  >
    <span v-if="$slots.leading" class="grid place-items-center"><slot name="leading" /></span>
    <slot />
    <span v-if="$slots.trailing" class="grid place-items-center"><slot name="trailing" /></span>
  </button>
</template>
<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'pill' | 'circle';
    size?: 'xs' | 'sm' | 'md' | 'lg';
    tone?: 'light' | 'muted' | 'white' | 'clear' | 'outline';
    active?: boolean;
    type?: 'button' | 'submit' | 'reset';
  }>(),
  {
    variant: 'pill',
    size: 'md',
    tone: 'light',
    active: false,
    type: 'button',
  },
);
</script>