<script setup lang="ts">
import BaseIcon from '@/components/common/BaseIcon.vue';

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
      class="grid h-5 w-5 shrink-0 place-items-center rounded-[7px] border border-border bg-surface text-text-inverse transition-colors peer-checked:border-primary peer-checked:bg-primary peer-checked:[&_svg]:opacity-100 peer-focus-visible:ring-2 peer-focus-visible:ring-primary/40"
    >
      <BaseIcon name="check" :size="12" class="opacity-0 transition-opacity" />
    </span>
    <span v-if="$slots.default" class="text-sm text-text-primary"><slot /></span>
  </label>
</template>
