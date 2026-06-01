<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue';

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
const isActive = computed(() => Boolean(props.modelValue));
const allOptions = computed(() => [
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

document.addEventListener('click', handleDocumentClick);

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick);
});
</script>

<template>
  <div ref="rootElement" :class="$style.dropdown">
    <button
      type="button"
      :class="[
        $style.trigger,
        isActive && $style.triggerActive,
        isOpen && $style.triggerOpen,
      ]"
      :aria-expanded="isOpen"
      :disabled="disabled"
      @click.stop="toggle"
    >
      <span :class="$style.label">{{ label }}</span>
      <span :class="$style.icon" aria-hidden="true">
        <svg viewBox="0 0 10 6">
          <path d="M4.625 5.025a.985.985 0 0 1-.231-.175L.107.563A.28.28 0 0 1 0 .35C-.004.267.032.188.107.113.182.037.257 0 .332 0s.15.037.225.113l4.337 4.337L9.232.113c.058-.059.129-.092.212-.1.083-.009.163.024.238.1.075.074.114.15.118.224.005.075-.031.15-.106.226L5.407 4.85a.984.984 0 0 1-.244.175 1.139 1.139 0 0 1-.538 0Z" fill="currentColor"/>
        </svg>
      </span>
    </button>

    <Transition :enter-active-class="$style.menuEnterActive" :enter-from-class="$style.menuEnterFrom" :leave-active-class="$style.menuLeaveActive" :leave-to-class="$style.menuLeaveTo">
      <div v-if="isOpen" :class="$style.menu">
        <button
          v-for="option in allOptions"
          :key="option.value || '__empty'"
          type="button"
          :class="[$style.option, option.value === modelValue && $style.optionActive]"
          @click="selectOption(option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </Transition>
  </div>
</template>

<style module lang="scss">
.dropdown {
  position: relative;
  z-index: 5;
  display: inline-flex;
}

.trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 104px;
  height: 34px;
  padding: 0 11px 0 15px;
  color: var(--color-text-primary);
  font-size: 13px;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  background: linear-gradient(180deg, #ffffff 0%, var(--color-surface-control) 100%);
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 999px;
  box-shadow: 0 1px 1px rgba(17, 24, 39, 0.04), inset 0 1px 0 rgba(255, 255, 255, 0.72);
  transition: color 0.18s ease, background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;

  &:hover {
    border-color: rgba(41, 69, 255, 0.2);
    box-shadow: 0 7px 18px rgba(17, 24, 39, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.84);
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.55;
  }
}

.triggerActive {
  color: var(--color-text-inverse);
  background: linear-gradient(180deg, #4961ff 0%, var(--color-primary) 100%);
  border-color: rgba(41, 69, 255, 0.45);
  box-shadow: 0 8px 18px rgba(41, 69, 255, 0.22);
}

.triggerOpen {
  border-color: rgba(41, 69, 255, 0.32);
  box-shadow: 0 10px 24px rgba(17, 24, 39, 0.12);
}

.label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.icon {
  display: grid;
  width: 20px;
  height: 20px;
  margin-left: 6px;
  place-items: center;
  color: currentColor;
  background: rgba(255, 255, 255, 0.42);
  border-radius: 999px;
  transition: transform 0.18s ease;

  svg {
    width: 10px;
    height: 6px;
  }
}

.triggerOpen .icon {
  transform: rotate(180deg);
}

.menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 100%;
  padding: 6px;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 18px;
  box-shadow: 0 18px 42px rgba(17, 24, 39, 0.14);
  backdrop-filter: blur(12px);
}

.option {
  display: flex;
  align-items: center;
  width: 100%;
  height: 30px;
  padding: 0 12px;
  color: var(--color-text-primary);
  font-size: 13px;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: 999px;
  transition: color 0.16s ease, background 0.16s ease;

  &:hover {
    background: var(--color-surface-control);
  }
}

.optionActive {
  color: var(--color-text-inverse);
  background: var(--color-primary);

  &:hover {
    background: var(--color-primary);
  }
}

.menuEnterActive,
.menuLeaveActive {
  transition: opacity 0.16s ease, transform 0.16s ease;
  transform-origin: top left;
}

.menuEnterFrom,
.menuLeaveTo {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}
</style>
