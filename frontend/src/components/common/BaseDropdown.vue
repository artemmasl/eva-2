<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';

import BaseIcon from '@/components/common/BaseIcon.vue';

interface BaseDropdownOption {
  label: string;
  value: string;
}

const props = withDefaults(
  defineProps<{
    modelValue?: string;
    options: BaseDropdownOption[];
    placeholder: string;
    resetLabel?: string;
    disabled?: boolean;
  }>(),
  {
    modelValue: '',
    resetLabel: '',
    disabled: false,
  },
);

const emit = defineEmits<{
  'update:modelValue': [value: string];
  change: [value: string];
}>();

const isOpen = ref(false);
const rootElement = ref<HTMLElement | null>(null);

const selectedOption = computed(() => props.options.find((option) => option.value === props.modelValue));
const label = computed(() => selectedOption.value?.label ?? props.placeholder);
const hasValue = computed(() => Boolean(props.modelValue));

const menuOptions = computed<BaseDropdownOption[]>(() => [
  { label: props.resetLabel || props.placeholder, value: '' },
  ...props.options,
]);

const close = () => {
  isOpen.value = false;
};

const toggle = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
  }
};

const selectOption = (value: string) => {
  emit('update:modelValue', value);
  emit('change', value);
  close();
};

const handleDocumentClick = (event: MouseEvent) => {
  if (!rootElement.value?.contains(event.target as Node)) {
    close();
  }
};

onMounted(() => document.addEventListener('click', handleDocumentClick));
onBeforeUnmount(() => document.removeEventListener('click', handleDocumentClick));
</script>

<template>
  <div ref="rootElement" class="relative inline-flex">
    <button
      type="button"
      :disabled="disabled"
      :aria-expanded="isOpen"
      :class="[
        'inline-flex h-9 min-w-[120px] cursor-pointer items-center justify-between gap-2 rounded-pill border px-4 text-[13px] leading-none transition-colors',
        hasValue
          ? 'border-primary bg-primary text-text-inverse'
          : 'border-border bg-surface text-text-primary hover:border-primary/40 hover:bg-surface-control',
        isOpen && !hasValue && 'border-primary/60',
        disabled && 'cursor-not-allowed opacity-60',
      ]"
      @click.stop="toggle"
    >
      <span class="truncate">{{ label }}</span>
      <BaseIcon
        name="chevron-down"
        :size="14"
        class="shrink-0 transition-transform duration-200"
        :class="isOpen && 'rotate-180'"
      />
    </button>

    <Transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-[0.98]"
      leave-active-class="transition duration-100 ease-in"
      leave-to-class="opacity-0 -translate-y-1 scale-[0.98]"
    >
      <div
        v-if="isOpen"
        class="absolute left-0 top-[calc(100%+6px)] z-30 min-w-full origin-top-left rounded-2xl border border-border bg-surface p-1.5 shadow-floating"
      >
        <button
          v-for="option in menuOptions"
          :key="option.value || '__reset'"
          type="button"
          :class="[
            'flex h-9 w-full cursor-pointer items-center whitespace-nowrap rounded-pill px-3 text-[13px] leading-none transition-colors',
            option.value === modelValue
              ? 'bg-primary text-text-inverse'
              : 'text-text-primary hover:bg-surface-control',
          ]"
          @click="selectOption(option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </Transition>
  </div>
</template>
