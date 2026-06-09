<script setup lang="ts">
import { computed, ref, watch } from 'vue';

const props = defineProps<{
  min: number;
  max: number;
  minValue?: number;
  maxValue?: number;
  step?: number;
  label: string;
  unit?: string;
}>();

const emit = defineEmits<{
  change: [range: { min?: number; max?: number }];
}>();

const localMin = ref(props.minValue ?? props.min);
const localMax = ref(props.maxValue ?? props.max);

const rangeStyle = computed(() => {
  const distance = props.max - props.min;
  const minPosition = distance > 0 ? ((localMin.value - props.min) / distance) * 100 : 0;
  const maxPosition = distance > 0 ? ((localMax.value - props.min) / distance) * 100 : 100;

  return {
    '--range-start': `${Math.max(0, Math.min(minPosition, 100))}%`,
    '--range-end': `${Math.max(0, Math.min(maxPosition, 100))}%`,
  };
});

watch(
  () => [props.minValue, props.maxValue, props.min, props.max],
  () => {
    localMin.value = props.minValue ?? props.min;
    localMax.value = props.maxValue ?? props.max;
  },
);

const formatValue = (value: number | undefined): string => {
  if (value === undefined) {
    return '—';
  }

  return new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(value);
};

const updateMin = (value: string) => {
  const nextMin = Number(value);
  const currentMax = localMax.value;

  localMin.value = Math.min(nextMin, currentMax);
};

const updateMax = (value: string) => {
  const nextMax = Number(value);
  const currentMin = localMin.value;

  localMax.value = Math.max(nextMax, currentMin);
};

const commitRange = () => {
  emit('change', {
    min: localMin.value === props.min ? undefined : localMin.value,
    max: localMax.value === props.max ? undefined : localMax.value,
  });
};
</script>

<template>
  <div class="grid w-full max-w-[260px] gap-2 rounded-[18px] border border-[#d9dce5] bg-white px-3 py-2 max-[900px]:min-w-0">
    <div class="flex items-center justify-between gap-3 text-xs text-[#111827] [&_strong]:whitespace-nowrap [&_strong]:font-medium">
      <span>{{ label }}</span>
      <strong class="w-[170px] shrink-0 text-right tabular-nums">{{ formatValue(localMin) }} — {{ formatValue(localMax) }}{{ unit ? ` ${unit}` : '' }}</strong>
    </div>

    <div
      class="relative h-[18px] before:absolute before:left-0 before:top-1/2 before:h-1 before:w-full before:-translate-y-1/2 before:rounded-full before:bg-[linear-gradient(to_right,var(--color-border)_0%,var(--color-border)_var(--range-start),var(--color-primary)_var(--range-start),var(--color-primary)_var(--range-end),var(--color-border)_var(--range-end),var(--color-border)_100%)] [&_input]:pointer-events-none [&_input]:absolute [&_input]:left-0 [&_input]:top-0 [&_input]:m-0 [&_input]:h-[18px] [&_input]:w-full [&_input]:appearance-none [&_input]:bg-transparent [&_input::-moz-range-thumb]:pointer-events-auto [&_input::-moz-range-thumb]:h-[18px] [&_input::-moz-range-thumb]:w-[18px] [&_input::-moz-range-thumb]:rounded-full [&_input::-moz-range-thumb]:border-0 [&_input::-moz-range-thumb]:bg-[var(--color-primary)] [&_input::-moz-range-track]:h-1 [&_input::-moz-range-track]:bg-transparent [&_input::-webkit-slider-runnable-track]:h-1 [&_input::-webkit-slider-runnable-track]:bg-transparent [&_input::-webkit-slider-thumb]:pointer-events-auto [&_input::-webkit-slider-thumb]:relative [&_input::-webkit-slider-thumb]:z-10 [&_input::-webkit-slider-thumb]:mt-[-7px] [&_input::-webkit-slider-thumb]:h-[18px] [&_input::-webkit-slider-thumb]:w-[18px] [&_input::-webkit-slider-thumb]:appearance-none [&_input::-webkit-slider-thumb]:rounded-full [&_input::-webkit-slider-thumb]:bg-[var(--color-primary)]"
      :style="rangeStyle"
    >
      <input
        :min="min"
        :max="max"
        :step="step ?? 1"
        :value="localMin"
        type="range"
        @input="updateMin(($event.target as HTMLInputElement).value)"
        @change="commitRange"
      />
      <input
        :min="min"
        :max="max"
        :step="step ?? 1"
        :value="localMax"
        type="range"
        @input="updateMax(($event.target as HTMLInputElement).value)"
        @change="commitRange"
      />
    </div>
  </div>
</template>
