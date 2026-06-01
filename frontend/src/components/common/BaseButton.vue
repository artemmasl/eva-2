<template>
  <button
    type="button"
    :class="[
      'inline-flex cursor-pointer items-center justify-center rounded-full border-0 font-normal leading-none transition-colors',
      size === 'xs' && 'min-h-[18px] px-2.5 text-[10px]',
      size === 'sm' && 'h-[22px] px-3 text-[11px]',
      size === 'md' && 'h-[34px] px-4 text-[13px]',
      size === 'lg' && 'h-[48px] px-8 text-base',
      variant === 'circle' && size === 'sm' && 'w-[22px] px-0',
      variant === 'circle' && size === 'md' && 'w-[34px] px-0',
      active
        ? 'bg-[#2945ff] text-white'
        : tone === 'clear'
          ? 'bg-transparent text-[#111827]'
          : tone === 'white'
            ? 'bg-white text-[#111827]'
            : tone === 'muted'
              ? 'bg-[#d9dce5] text-[#111827]'
              : 'bg-[#f3f4f6] text-[#111827]',
    ]"
  >
    <slot />
  </button>
</template>
<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'pill' | 'circle';
    size?: 'xs' | 'sm' | 'md' | 'lg';
    tone?: 'light' | 'muted' | 'white' | 'clear';
    active?: boolean;
  }>(),
  {
    variant: 'pill',
    size: 'md',
    tone: 'light',
    active: false,
  },
);
</script>