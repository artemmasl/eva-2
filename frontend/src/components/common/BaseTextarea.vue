<script setup lang="ts">
withDefaults(
  defineProps<{
    placeholder?: string;
    rows?: number;
    disabled?: boolean;
    invalid?: boolean;
    id?: string;
  }>(),
  {
    placeholder: '',
    rows: 4,
    disabled: false,
    invalid: false,
    id: undefined,
  },
);

const model = defineModel<string>({ default: '' });
</script>

<template>
  <textarea
    :id="id"
    v-model="model"
    :rows="rows"
    :placeholder="placeholder"
    :disabled="disabled"
    :class="[
      'w-full resize-y rounded-control border bg-surface-control px-4 py-3 text-sm text-text-primary outline-none transition-colors placeholder:text-text-secondary',
      'focus:border-primary focus:bg-surface',
      invalid ? 'border-accent' : 'border-transparent',
      disabled && 'cursor-not-allowed opacity-60',
    ]"
  />
</template>
