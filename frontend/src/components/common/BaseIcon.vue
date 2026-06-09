<script setup lang="ts">
import { computed, type Component } from 'vue';

const props = withDefaults(
  defineProps<{
    name: string;
    size?: number | string;
  }>(),
  {
    size: 20,
  },
);

const modules = import.meta.glob('../../assets/icons/*.svg', {
  eager: true,
  query: '?component',
  import: 'default',
}) as Record<string, Component>;

const registry: Record<string, Component> = Object.fromEntries(
  Object.entries(modules).map(([path, component]) => [
    path.split('/').pop()?.replace('.svg', '') ?? path,
    component,
  ]),
);

const icon = computed<Component | undefined>(() => registry[props.name]);

const dimension = computed(() => (typeof props.size === 'number' ? String(props.size) : props.size));
</script>

<template>
  <component
    :is="icon"
    v-if="icon"
    :width="dimension"
    :height="dimension"
    aria-hidden="true"
    focusable="false"
  />
</template>
