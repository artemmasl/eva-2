<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import { adminApi } from '@/core/api/admin.api';
import type { Lead, LeadKind } from '@/core/entities/lead/types';
import { useAdminStore } from '@/stores/modules/admin.store';

const adminStore = useAdminStore();

const status = ref<'loading' | 'ready' | 'error'>('loading');
const leads = ref<Lead[]>([]);

const KIND_LABELS: Record<LeadKind, string> = {
  callback: 'Обратный звонок',
  consultation: 'Консультация',
  booking: 'Бронирование',
  conditions: 'Условия покупки',
};

const kindLabel = (kind: LeadKind) => KIND_LABELS[kind] ?? kind;

const formatDate = (value: string) => {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const hasLeads = computed(() => leads.value.length > 0);

onMounted(async () => {
  if (!adminStore.token) {
    return;
  }

  status.value = 'loading';

  try {
    leads.value = await adminApi.listLeads(adminStore.token);
    status.value = 'ready';
  } catch {
    status.value = 'error';
  }
});
</script>

<template>
  <section class="flex flex-col gap-6">
    <header class="flex flex-col gap-1">
      <h1 class="m-0 text-2xl font-semibold text-text-primary">Заявки</h1>
      <p class="m-0 text-sm text-text-secondary">Обратные звонки, консультации и бронирования с витрины</p>
    </header>

    <p v-if="status === 'loading'" class="text-sm text-text-secondary">Загрузка…</p>
    <p v-else-if="status === 'error'" class="text-sm text-accent">Не удалось загрузить заявки</p>

    <p v-else-if="!hasLeads" class="rounded-card bg-surface p-8 text-center text-sm text-text-secondary shadow-card">
      Заявок пока нет
    </p>

    <div v-else class="grid gap-3">
      <article
        v-for="lead in leads"
        :key="lead.id"
        class="flex flex-col gap-3 rounded-card bg-surface p-5 shadow-card"
      >
        <div class="flex flex-wrap items-center justify-between gap-3">
          <span class="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
            {{ kindLabel(lead.kind) }}
          </span>
          <span class="text-xs text-text-secondary">{{ formatDate(lead.created_at) }}</span>
        </div>

        <div class="flex flex-wrap items-center gap-x-6 gap-y-1">
          <span class="text-base font-semibold text-text-primary">{{ lead.name || 'Без имени' }}</span>
          <a v-if="lead.phone" :href="`tel:${lead.phone}`" class="text-sm text-primary no-underline hover:underline">
            {{ lead.phone }}
          </a>
        </div>

        <p v-if="lead.comment" class="m-0 text-sm text-text-secondary">{{ lead.comment }}</p>

        <div class="flex flex-wrap gap-x-4 gap-y-1 text-xs text-text-secondary">
          <span v-if="lead.developer_slug">Застройщик: {{ lead.developer_slug }}</span>
          <span v-if="lead.complex_id">ЖК: {{ lead.complex_id }}</span>
          <span v-if="lead.space_id">Помещение: {{ lead.space_id }}</span>
        </div>
      </article>
    </div>
  </section>
</template>
