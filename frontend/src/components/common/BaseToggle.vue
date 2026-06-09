<script setup lang="ts">
withDefaults(
  defineProps<{
    disabled?: boolean;
  }>(),
  {
    disabled: false,
  },
);

const model = defineModel<boolean>({ default: false });
</script>

<template>
  <label
    :class="[
      'inline-flex select-none items-center gap-2.5',
      disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer',
    ]"
  >
    <input
      v-model="model"
      type="checkbox"
      class="peer sr-only"
      :disabled="disabled"
    />
    <span
      class="relative h-6 w-11 shrink-0 rounded-pill bg-border transition-colors peer-checked:bg-primary peer-checked:[&>span]:translate-x-5 peer-focus-visible:ring-2 peer-focus-visible:ring-primary/40"
    >
      <span class="absolute left-0.5 top-0.5 h-5 w-5 rounded-full bg-white shadow-[0_2px_6px_rgba(15,23,42,0.25)] transition-transform" />
    </span>
    <span v-if="$slots.default" class="text-sm text-text-primary"><slot /></span>
  </label>
</template>
