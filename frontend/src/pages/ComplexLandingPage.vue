<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import ComplexesMap from '@/components/complexes/ComplexesMap.vue';
import type { ComplexSummary, RoomGroupStat } from '@/core/entities/complex/types';
import { useCatalogStore } from '@/stores/modules/catalog.store';
import { useComplexStore } from '@/stores/modules/complex.store';

const route = useRoute();
const router = useRouter();
const catalogStore = useCatalogStore();
const complexStore = useComplexStore();

const complex = computed(() => complexStore.current);
const complexesForMap = computed<ComplexSummary[]>(() => (complex.value ? [complex.value] : []));

const FLAT_GROUP_LABELS: Record<string, string> = {
  studio: 'Квартир-студий',
  one: 'Однокомнатных квартир',
  two: 'Двухкомнатных квартир',
  three: 'Трёхкомнатных квартир',
  four_plus: 'Многокомнатных квартир',
};

const flatGroups = computed<RoomGroupStat[]>(() => (
  complex.value?.stats.room_groups.filter((group) => group.key in FLAT_GROUP_LABELS) ?? []
));

interface HeaderStat {
  key: string;
  count: number;
  label: string;
}

const headerStats = computed<HeaderStat[]>(() => {
  if (!complex.value) {
    return [];
  }

  if (flatGroups.value.length >= 2) {
    return flatGroups.value.map((group) => ({
      key: group.key,
      count: group.count,
      label: FLAT_GROUP_LABELS[group.key],
    }));
  }

  return [{
    key: 'all',
    count: complex.value.stats.flats_for_sale,
    label: 'Квартир разной планировки',
  }];
});

const statusLabel = computed(() => (
  complex.value && complex.value.stats.flats_for_sale > 0
    ? 'Сейчас в продаже'
    : complex.value?.delivery_status ?? ''
));

const brandMark = computed(() => (complex.value?.name.trim().charAt(0) || 'A').toUpperCase());

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

type TypeFilters = { stype: string; is_apartment?: boolean; rooms?: number };

const spaceTypeTabs: { label: string; filters: TypeFilters }[] = [
  { label: 'Квартиры', filters: { stype: 'flat', is_apartment: false } },
  { label: 'Парковки', filters: { stype: 'parking' } },
  { label: 'Кладовки', filters: { stype: 'storage' } },
  { label: 'Коммерция', filters: { stype: 'commercial' } },
];

const PLAN_ROOMS: Record<string, number> = {
  studio: 0,
  one: 1,
  two: 2,
  three: 3,
  four_plus: 4,
};

const goToCatalog = (filters: TypeFilters) => {
  if (!complex.value) {
    return;
  }

  catalogStore.setFilters({ ...filters });
  void router.push({ name: 'catalog', params: { complexId: complex.value.id } });
};

const openPlanGroup = (group: RoomGroupStat) => {
  goToCatalog({ stype: 'flat', is_apartment: false, rooms: PLAN_ROOMS[group.key] ?? 0 });
};

const infrastructure = [
  { title: 'Школы и детсады', text: 'Школы и детские сады в пешей доступности.' },
  { title: 'Парки и набережная', text: 'Зелёная зона для прогулок в 5 минутах.' },
  { title: 'Магазины и сервисы', text: 'Супермаркеты, аптеки и кафе на первых этажах.' },
  { title: 'Транспорт', text: 'Остановки рядом и удобный выезд на магистраль.' },
];

const loadCurrent = (complexId: unknown) => {
  if (complexId) {
    void complexStore.loadComplex(String(complexId));
  }
};

onMounted(() => loadCurrent(route.params.complexId));
watch(() => route.params.complexId, loadCurrent);
</script>

<template>
  <main class="mx-auto flex w-full grow flex-col gap-8" :class="$style.page">
    <p v-if="complexStore.isLoading && !complex" :class="$style.state">Загрузка…</p>
    <p v-else-if="!complex" :class="$style.state">Комплекс не найден</p>

    <template v-else>
      <section :class="$style.cover">
        <div :class="$style.coverScrim" />

        <div :class="$style.coverContent">
          <div class="flex items-center justify-center gap-5">
            <span :class="$style.logoMark">{{ brandMark }}</span>
            <h1 :class="$style.title">{{ complex.name }}</h1>
          </div>

          <p :class="$style.address">{{ complex.address }}</p>

          <span v-if="statusLabel" :class="$style.statusPill">{{ statusLabel }}</span>
        </div>

        <div :class="$style.statsRow">
          <div v-for="stat in headerStats" :key="stat.key" :class="$style.statItem">
            <span :class="$style.statCount">{{ stat.count }}</span>
            <span :class="$style.statLabel">{{ stat.label }}</span>
          </div>
        </div>
      </section>

      <nav :class="$style.tabs">
        <button
          v-for="tab in spaceTypeTabs"
          :key="tab.label"
          type="button"
          :class="$style.tab"
          @click="goToCatalog(tab.filters)"
        >
          {{ tab.label }}
        </button>
      </nav>

      <section class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex flex-col gap-1">
          <span :class="$style.metaLine">{{ complex.district }} · {{ complex.metro }} · {{ complex.metro_time }}</span>
          <span v-if="complex.stats.price_from !== null" :class="$style.metaPrice">
            Квартиры от {{ formatPrice(complex.stats.price_from) }}
          </span>
        </div>

        <RouterLink
          :class="$style.cta"
          :to="{ name: 'catalog', params: { complexId: complex.id } }"
        >
          Смотреть квартиры
        </RouterLink>
      </section>

      <section :class="$style.section">
        <h2 :class="$style.sectionTitle">О проекте</h2>
        <p :class="$style.sectionText">
          «{{ complex.name }}» — современный жилой комплекс в районе {{ complex.district }}.
          Рядом {{ complex.metro }} ({{ complex.metro_time }}). Продуманные планировки,
          благоустроенная территория и развитая инфраструктура для комфортной жизни.
        </p>
        <div :class="$style.facts">
          <div :class="$style.fact">
            <span :class="$style.factValue">{{ statusLabel }}</span>
            <span :class="$style.factLabel">Статус</span>
          </div>
          <div :class="$style.fact">
            <span :class="$style.factValue">{{ complex.stats.flats_for_sale }}</span>
            <span :class="$style.factLabel">Квартир в продаже</span>
          </div>
          <div :class="$style.fact">
            <span :class="$style.factValue">{{ complex.district }}</span>
            <span :class="$style.factLabel">Район</span>
          </div>
          <div :class="$style.fact">
            <span :class="$style.factValue">{{ complex.metro }}</span>
            <span :class="$style.factLabel">Метро</span>
          </div>
        </div>
      </section>

      <section :class="$style.section">
        <h2 :class="$style.sectionTitle">Галерея</h2>
        <div :class="$style.gallery">
          <div v-for="n in 4" :key="n" :class="$style.galleryTile" />
        </div>
      </section>

      <section v-if="flatGroups.length" :class="$style.section">
        <h2 :class="$style.sectionTitle">Планировки квартир</h2>
        <div :class="$style.planGrid">
          <button
            v-for="group in flatGroups"
            :key="group.key"
            type="button"
            :class="$style.planCard"
            @click="openPlanGroup(group)"
          >
            <span :class="$style.planLabel">{{ group.label }}</span>
            <span :class="$style.planCount">{{ group.count }} в продаже</span>
            <span :class="$style.planMeta">от {{ formatArea(group.area_from) }} · от {{ formatPrice(group.price_from) }}</span>
          </button>
        </div>
      </section>

      <section :class="$style.section">
        <h2 :class="$style.sectionTitle">Инфраструктура района</h2>
        <div :class="$style.infraGrid">
          <div v-for="item in infrastructure" :key="item.title" :class="$style.infraCard">
            <span :class="$style.infraTitle">{{ item.title }}</span>
            <span :class="$style.infraText">{{ item.text }}</span>
          </div>
        </div>
      </section>

      <section :class="$style.section">
        <h2 :class="$style.sectionTitle">Расположение</h2>
        <p :class="$style.sectionText">{{ complex.address }}</p>
        <ComplexesMap :complexes="complexesForMap" />
      </section>
    </template>
  </main>
</template>

<style module lang="scss">
.page {
  max-width: 1328px;
}

.state {
  padding: 40px;
  color: var(--color-text-secondary);
  text-align: center;
  background: var(--color-surface);
  border-radius: 24px;
}

.cover {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 420px;
  padding: 48px 32px 28px;
  overflow: hidden;
  border-radius: 32px;
  background: linear-gradient(135deg, #1f2a44 0%, #3a4d7a 55%, #6b7fb0 100%);
}

.coverScrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(8, 15, 31, 0.15) 0%, rgba(8, 15, 31, 0.45) 100%);
}

.coverContent {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  align-items: center;
  justify-content: center;
  gap: 16px;
  text-align: center;
}

.logoMark {
  display: grid;
  place-items: center;
  width: 64px;
  height: 64px;
  font-size: 26px;
  font-weight: 800;
  color: var(--color-primary);
  background: #fff;
  border-radius: 50%;
}

.title {
  margin: 0;
  font-size: 48px;
  font-weight: 700;
  color: #fff;

  @media (max-width: 720px) {
    font-size: 32px;
  }
}

.address {
  margin: 0;
  font-size: 17px;
  color: rgba(255, 255, 255, 0.82);
}

.statusPill {
  padding: 8px 18px;
  font-size: 14px;
  color: var(--color-text-inverse);
  background: var(--color-primary);
  border-radius: var(--radius-pill);
}

.statsRow {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 48px;
  margin-top: 24px;

  @media (max-width: 720px) {
    gap: 28px;
  }
}

.statItem {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.statCount {
  font-size: 34px;
  font-weight: 700;
  color: #fff;
}

.statLabel {
  max-width: 140px;
  font-size: 14px;
  line-height: 1.25;
  color: rgba(255, 255, 255, 0.82);
}

.metaLine {
  font-size: 15px;
  color: var(--color-text-secondary);
}

.metaPrice {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.cta {
  padding: 14px 28px;
  font-weight: 600;
  color: var(--color-text-inverse);
  text-decoration: none;
  background: var(--color-primary);
  border-radius: var(--radius-pill);
  transition: transform 140ms ease;

  &:hover {
    transform: translateY(-2px);
  }
}

.tabs {
  position: sticky;
  top: 16px;
  z-index: 10;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-self: flex-start;
  padding: 8px;
  background: var(--color-surface);
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-card);
}

.tab {
  padding: 10px 22px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: var(--radius-pill);
  transition: background 140ms ease, color 140ms ease;

  &:hover {
    color: var(--color-text-primary);
    background: var(--color-surface-control);
  }
}

.section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sectionTitle {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.sectionText {
  margin: 0;
  max-width: 760px;
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

.facts {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;

  @media (max-width: 720px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.fact {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 20px;
  background: var(--color-surface);
  border-radius: 20px;
  box-shadow: var(--shadow-card);
}

.factValue {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.factLabel {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.gallery {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;

  @media (max-width: 720px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.galleryTile {
  height: 180px;
  border-radius: 20px;
  background: linear-gradient(135deg, #2b3a5e 0%, #6b7fb0 100%);
}

.planGrid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.planCard {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 22px;
  text-align: left;
  cursor: pointer;
  background: var(--color-surface);
  border: 1px solid transparent;
  border-radius: 20px;
  box-shadow: var(--shadow-card);
  transition: border-color 140ms ease, transform 140ms ease;

  &:hover {
    border-color: var(--color-primary);
    transform: translateY(-2px);
  }
}

.planLabel {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.planCount {
  font-size: 14px;
  color: var(--color-primary);
}

.planMeta {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.infraGrid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;

  @media (max-width: 720px) {
    grid-template-columns: 1fr;
  }
}

.infraCard {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 20px;
  background: var(--color-surface);
  border-radius: 20px;
  box-shadow: var(--shadow-card);
}

.infraTitle {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.infraText {
  font-size: 14px;
  line-height: 1.45;
  color: var(--color-text-secondary);
}
</style>
