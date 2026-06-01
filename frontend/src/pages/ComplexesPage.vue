<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import ComplexesMap from '@/components/complexes/ComplexesMap.vue';
import type { ComplexSummary } from '@/core/entities/complex/types';
import { getComplexes } from '@/core/entities/complex/use-cases';

const route = useRoute();
const complexes = ref<ComplexSummary[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

const isMapView = computed(() => route.query.view === 'map');

const formatPrice = (amount: number): string => (
  new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0,
  }).format(amount)
);

const formatArea = (value: number): string => (
  `${new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(value)} м²`
);

const flatsLabel = (count: number): string => {
  const mod100 = count % 100;
  const mod10 = count % 10;
  const word = mod100 >= 11 && mod100 <= 14
    ? 'квартир'
    : mod10 === 1
      ? 'квартира'
      : mod10 >= 2 && mod10 <= 4
        ? 'квартиры'
        : 'квартир';

  return `${count} ${word} в продаже`;
};

onMounted(async () => {
  isLoading.value = true;
  error.value = null;

  try {
    complexes.value = await getComplexes();
  } catch {
    error.value = 'Не удалось загрузить жилые комплексы';
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <main class="mx-auto flex w-full grow flex-col gap-6" :class="$style.page">
    <header class="flex items-center justify-between gap-4">
      <h1 class="text-2xl font-semibold" :class="$style.title">Все жилые комплексы</h1>
      <div class="flex rounded-full p-1" :class="$style.viewToggle">
        <RouterLink :class="[$style.viewOption, !isMapView && $style.viewOptionActive]" :to="{ name: 'complexes' }">Список</RouterLink>
        <RouterLink :class="[$style.viewOption, isMapView && $style.viewOptionActive]" :to="{ name: 'complexes', query: { view: 'map' } }">На карте</RouterLink>
      </div>
    </header>

    <p v-if="isLoading" :class="$style.state">Загрузка…</p>
    <p v-else-if="error" :class="$style.state">{{ error }}</p>

    <ComplexesMap v-else-if="isMapView" :complexes="complexes" />

    <section v-else class="grid gap-6" :class="$style.grid">
      <RouterLink
        v-for="complex in complexes"
        :key="complex.id"
        class="flex flex-col overflow-hidden rounded-3xl no-underline"
        :class="$style.card"
        :to="{ name: 'complex-landing', params: { complexId: complex.id } }"
      >
        <div :class="$style.cover">
          <span :class="$style.status">{{ complex.delivery_status }}</span>
          <span :class="$style.coverMark">{{ complex.name.charAt(0) }}</span>
        </div>

        <div class="flex flex-col gap-3 p-6">
          <div class="flex items-start justify-between gap-4">
            <div class="flex flex-wrap items-center gap-2.5">
              <h2 class="text-xl font-semibold" :class="$style.cardTitle">{{ complex.name }}</h2>
              <span :class="$style.salesBadge">{{ flatsLabel(complex.stats.flats_for_sale) }}</span>
            </div>
            <span v-if="complex.stats.price_from !== null" class="whitespace-nowrap text-base font-semibold" :class="$style.price">
              от {{ formatPrice(complex.stats.price_from) }}
            </span>
          </div>

          <p :class="$style.location">{{ complex.district }}, {{ complex.metro }}, {{ complex.metro_time }}</p>

          <div v-if="complex.stats.room_groups.length" :class="$style.stats">
            <div :class="$style.statsGrid">
              <div v-for="group in complex.stats.room_groups" :key="group.key" :class="$style.statRow">
                <span :class="$style.statLabel">{{ group.label }}</span>
                <span :class="$style.statArea">от {{ formatArea(group.area_from) }}</span>
                <span :class="$style.statPrice">от {{ formatPrice(group.price_from) }}</span>
              </div>
            </div>
          </div>
        </div>
      </RouterLink>
    </section>
  </main>
</template>

<style module lang="scss">
.page {
  max-width: 1328px;
}

.title {
  color: var(--color-text-primary);
}

.viewToggle {
  background: var(--color-surface-control);
}

.viewOption {
  padding: 8px 18px;
  color: var(--color-text-secondary);
  font-size: 14px;
  text-decoration: none;
  border-radius: var(--radius-pill);
}

.viewOptionActive {
  color: var(--color-text-inverse);
  background: var(--color-primary);
}

.state {
  padding: 40px;
  color: var(--color-text-secondary);
  text-align: center;
  background: var(--color-surface);
  border-radius: 24px;
}

.grid {
  grid-template-columns: repeat(auto-fill, minmax(440px, 1fr));

  @media (max-width: 720px) {
    grid-template-columns: 1fr;
  }
}

.card {
  color: var(--color-text-primary);
  background: var(--color-surface);
  box-shadow: var(--shadow-card);
  transition: transform 180ms ease, box-shadow 180ms ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-header);
  }
}

.cover {
  position: relative;
  display: grid;
  place-items: center;
  height: 220px;
  background: linear-gradient(135deg, #1f2a44 0%, #3a4d7a 55%, #6b7fb0 100%);
}

.coverMark {
  font-size: 96px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.16);
}

.status {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 14px;
  font-size: 12px;
  color: var(--color-text-inverse);
  background: color-mix(in srgb, var(--color-primary) 92%, transparent);
  border-radius: var(--radius-pill);
}

.cardTitle {
  color: var(--color-text-primary);
}

.salesBadge {
  padding: 5px 12px;
  font-size: 12px;
  color: var(--color-text-secondary);
  background: var(--color-surface-control);
  border-radius: var(--radius-pill);
}

.price {
  color: var(--color-text-primary);
}

.location {
  font-size: 14px;
  color: var(--color-primary);
}

.stats {
  display: grid;
  grid-template-rows: 0fr;
  margin-top: 0;
  opacity: 0;
  transition: grid-template-rows 220ms ease, opacity 220ms ease, margin-top 220ms ease;
}

.card:hover .stats {
  grid-template-rows: 1fr;
  margin-top: 6px;
  opacity: 1;
}

.statsGrid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 28px;
  min-height: 0;
  overflow: hidden;
  padding-top: 12px;
  border-top: 1px solid var(--color-surface-control);
}

.statRow {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 10px;
  align-items: baseline;
  font-size: 12px;
}

.statLabel {
  color: var(--color-primary);
}

.statArea {
  color: var(--color-text-secondary);
}

.statPrice {
  color: var(--color-text-primary);
  white-space: nowrap;
}
</style>
