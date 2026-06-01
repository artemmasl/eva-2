<template>
  <div
    v-motion
    class="fixed inset-0 z-[100] grid place-items-center bg-[rgba(17,17,17,0.48)] p-8 transition-colors duration-200 ease-in-out max-[900px]:items-end max-[900px]:p-0"
    :initial="{ opacity: 0 }"
    :enter="{ opacity: 1, transition: { duration: 180, ease: 'easeOut' } }"
    @click.self="emit('close')"
  >
    <section
      v-motion
      :class="panelClass"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="labelledBy"
      :initial="{ opacity: 0, scale: 0.98, y: 18 }"
      :enter="{ opacity: 1, scale: 1, y: 0, transition: { duration: 260, ease: 'easeOut' } }"
    >
      <slot />
    </section>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  labelledBy?: string;
  panelClass?: string;
}>();

const emit = defineEmits<{
  close: [];
}>();
</script>
