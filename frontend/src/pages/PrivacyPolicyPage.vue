<script setup lang="ts">
import { computed } from 'vue';

import { useTenantStore } from '@/stores/modules/tenant.store';

const tenantStore = useTenantStore();

const developer = computed(() => tenantStore.tenant?.developer ?? null);
const developerName = computed(() => developer.value?.name ?? '');
const policyText = computed(() => developer.value?.privacy_policy?.trim() ?? '');
</script>

<template>
  <main class="mx-auto w-full max-w-[820px] px-6 py-12">
    <h1 class="m-0 mb-2 text-3xl font-semibold text-text-primary">Политика конфиденциальности</h1>
    <p v-if="developerName" class="m-0 mb-8 text-sm text-text-secondary">{{ developerName }}</p>

    <article
      v-if="policyText"
      class="whitespace-pre-wrap text-[15px] leading-relaxed text-text-primary"
    >{{ policyText }}</article>

    <p v-else class="rounded-card bg-surface p-8 text-center text-sm text-text-secondary shadow-card">
      Текст политики конфиденциальности пока не заполнен.
    </p>
  </main>
</template>
