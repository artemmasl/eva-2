<script setup lang="ts">
import BaseIcon from '@/components/common/BaseIcon.vue';
import BaseInput from '@/components/common/BaseInput.vue';

const search = defineModel<string>({ required: true });
</script>

<template>
  <div class="w-full max-w-[680px]">
    <BaseInput v-model="search" type="search" size="lg" tone="surface" placeholder="Поиск помещений">
      <template #leading>
        <BaseIcon name="search" :size="18" />
      </template>
    </BaseInput>
  </div>
</template>
