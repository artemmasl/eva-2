<script setup lang="ts">
import { vMaska } from 'maska/vue';
import { computed, useSlots } from 'vue';

const props = withDefaults(
  defineProps<{
    type?: string;
    placeholder?: string;
    size?: 'sm' | 'md' | 'lg';
    tone?: 'control' | 'surface';
    disabled?: boolean;
    invalid?: boolean;
    mask?: string;
    id?: string;
  }>(),
  {
    type: 'text',
    placeholder: '',
    size: 'md',
    tone: 'control',
    disabled: false,
    invalid: false,
    mask: undefined,
    id: undefined,
  },
);

const model = defineModel<string | number>({ default: '' });

const slots = useSlots();

const sizeClass = computed(() => ({
  sm: 'h-9 text-[13px]',
  md: 'h-11 text-sm',
  lg: 'h-12 text-base',
}[props.size]));
</script>

<template>
  <label
    :class="[
      'inline-flex w-full items-center gap-2 rounded-control border px-4 transition-colors focus-within:border-primary',
      tone === 'surface' ? 'bg-surface shadow-card' : 'bg-surface-control focus-within:bg-surface',
      invalid ? 'border-accent' : tone === 'surface' ? 'border-border' : 'border-transparent',
      disabled && 'cursor-not-allowed opacity-60',
      sizeClass,
    ]"
  >
    <span v-if="slots.leading" class="grid shrink-0 place-items-center text-text-secondary">
      <slot name="leading" />
    </span>

    <input
      :id="id"
      v-model="model"
      v-maska="mask"
      class="min-w-0 flex-1 border-0 bg-transparent text-text-primary outline-none placeholder:text-text-secondary"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
    />

    <span v-if="slots.trailing" class="grid shrink-0 place-items-center text-text-secondary">
      <slot name="trailing" />
    </span>
  </label>
</template>
