<template>
  <div
    :class="[
      'inline-flex overflow-hidden rounded-full bg-[#d9dce5]',
      size === 'sm' && 'h-[34px]',
      size === 'md' && 'h-[40px]',
    ]"
  >
    <BaseButton
      v-for="option in options"
      :key="String(option.value)"
      :class="[
        'rounded-none',
        size === 'sm' && 'h-[34px] px-5 text-[11px]',
        size === 'md' && 'h-[40px] px-6 text-[13px]',
      ]"
      size="md"
      tone="clear"
      :active="modelValue === option.value"
      @click="emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </BaseButton>
  </div>
</template>

<script setup lang="ts">
import BaseButton from '@/components/common/BaseButton.vue';

defineProps<{
  modelValue: string | number | boolean;
  options: {
    label: string;
    value: string | number | boolean;
  }[];
  size?: 'sm' | 'md';
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string | number | boolean];
}>();
</script>
