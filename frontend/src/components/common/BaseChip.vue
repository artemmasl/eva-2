<script setup lang="ts">
import { computed } from 'vue';

import BaseIcon from '@/components/common/BaseIcon.vue';

const props = withDefaults(
  defineProps<{
    active?: boolean;
    removable?: boolean;
    disabled?: boolean;
    size?: 'sm' | 'md';
  }>(),
  {
    active: false,
    removable: false,
    disabled: false,
    size: 'md',
  },
);

const emit = defineEmits<{
  click: [];
  remove: [];
}>();

const sizeClass = computed(() => (props.size === 'sm' ? 'h-7 px-3 text-xs' : 'h-9 px-4 text-[13px]'));
</script>

<template>
  <button
    type="button"
    :disabled="disabled"
    :class="[
      'inline-flex cursor-pointer items-center gap-1.5 rounded-pill border font-normal leading-none transition-colors',
      sizeClass,
      active
        ? 'border-primary bg-primary text-text-inverse'
        : 'border-border bg-surface text-text-primary hover:border-primary/40 hover:bg-surface-control',
      disabled && 'cursor-not-allowed opacity-60',
    ]"
    @click="emit('click')"
  >
    <slot />
    <span
      v-if="removable"
      class="grid h-4 w-4 place-items-center rounded-full text-current/80 hover:text-current"
      aria-hidden="true"
      @click.stop="emit('remove')"
    >
      <BaseIcon name="close" :size="10" />
    </span>
  </button>
</template>
