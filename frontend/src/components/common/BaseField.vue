<script setup lang="ts">
defineProps<{
  label?: string;
  hint?: string;
  error?: string;
  required?: boolean;
  htmlFor?: string;
}>();
</script>

<template>
  <div class="grid gap-1.5">
    <label v-if="label" :for="htmlFor" class="text-[13px] font-medium text-text-primary">
      {{ label }}<span v-if="required" class="text-accent"> *</span>
    </label>

    <slot />

    <span v-if="error" class="text-xs text-accent">{{ error }}</span>
    <span v-else-if="hint" class="text-xs text-text-secondary">{{ hint }}</span>
  </div>
</template>
