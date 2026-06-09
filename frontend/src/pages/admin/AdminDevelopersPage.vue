<script setup lang="ts">
import { onMounted, ref } from 'vue';

import { adminApi } from '@/core/api/admin.api';
import type { Developer } from '@/core/entities/developer/types';
import { useAdminStore } from '@/stores/modules/admin.store';

const adminStore = useAdminStore();

const developers = ref<Developer[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

onMounted(async () => {
  if (!adminStore.token) {
    return;
  }

  isLoading.value = true;
  error.value = null;

  try {
    developers.value = await adminApi.listDevelopers(adminStore.token);
  } catch {
    error.value = 'Не удалось загрузить застройщиков';
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <section class="flex flex-col gap-6">
    <header class="flex flex-col gap-1">
      <h1 class="m-0 text-2xl font-semibold text-text-primary">Застройщики</h1>
      <p class="m-0 text-sm text-text-secondary">Базовая информация и глобальные стили витрины</p>
    </header>

    <p v-if="isLoading" class="text-sm text-text-secondary">Загрузка…</p>
    <p v-else-if="error" class="text-sm text-accent">{{ error }}</p>

    <div v-else class="grid gap-3">
      <RouterLink
        v-for="developer in developers"
        :key="developer.id"
        :to="{ name: 'admin-developer-edit', params: { developerId: developer.id } }"
        class="flex items-center justify-between gap-4 rounded-card bg-surface p-5 no-underline shadow-card transition-shadow hover:shadow-header"
      >
        <div class="flex items-center gap-4">
          <img
            v-if="developer.logo"
            :src="developer.logo"
            alt=""
            class="h-12 w-12 rounded-control object-cover"
          />
          <span
            v-else
            class="grid h-12 w-12 place-items-center rounded-control text-lg font-bold text-text-inverse"
            :style="{ background: developer.theme_config.primaryColor }"
          >
            {{ developer.name.charAt(0) }}
          </span>

          <div class="flex flex-col">
            <span class="text-base font-semibold text-text-primary">{{ developer.name }}</span>
            <span class="text-[13px] text-text-secondary">/{{ developer.slug }} · {{ developer.phone }}</span>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <span
            class="h-6 w-6 rounded-full border border-border"
            :style="{ background: developer.theme_config.primaryColor }"
            :title="developer.theme_config.primaryColor"
          />
          <span class="text-text-secondary">→</span>
        </div>
      </RouterLink>
    </div>
  </section>
</template>
