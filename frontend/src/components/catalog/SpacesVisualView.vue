<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import PlanViewer from '@/components/plans/PlanViewer.vue';
import type { PlanAsset, PlanRegion } from '@/core/entities/plan/types';
import { getPlanWithRegions } from '@/core/entities/plan/use-cases';
import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useCatalogStore } from '@/stores/modules/catalog.store';

const route = useRoute();
const router = useRouter();
const link = useStorefrontLink();
const catalogStore = useCatalogStore();

const status = ref<'loading' | 'ready' | 'empty'>('loading');
const asset = ref<PlanAsset | null>(null);
const regions = ref<PlanRegion[]>([]);
const selected = ref<PlanRegion | null>(null);

const complexId = computed(() => (route.params.complexId ? String(route.params.complexId) : ''));

const load = async () => {
  status.value = 'loading';
  selected.value = null;

  if (!complexId.value) {
    status.value = 'empty';
    return;
  }

  const result = await getPlanWithRegions({ complex_id: complexId.value, kind: 'masterplan' });

  if (!result) {
    asset.value = null;
    regions.value = [];
    status.value = 'empty';
    return;
  }

  asset.value = result.asset;
  regions.value = result.regions.filter((region) => region.target_kind === 'building');
  status.value = 'ready';
};

const onSelect = (region: PlanRegion) => {
  if (region.status !== 'available') {
    return;
  }

  selected.value = region;
};

const openBuilding = (region: PlanRegion) => {
  catalogStore.updateFilters({ building_id: region.target_id });
  void router.push(link({ name: 'catalog', params: { complexId: complexId.value }, query: {} }));
};

const openBuildingViz = (region: PlanRegion) => {
  void router.push(link({ name: 'building-viz', params: { complexId: complexId.value, buildingId: region.target_id } }));
};

onMounted(load);
watch(complexId, load);
</script>

<template>
  <section v-if="status === 'loading'" :class="$style.placeholder">
    <p :class="$style.text">Загрузка генплана…</p>
  </section>

  <section v-else-if="status === 'empty'" :class="$style.placeholder">
    <h2 :class="$style.title">Визуальный подбор недоступен</h2>
    <p :class="$style.text">Для этого комплекса ещё не загружен генплан. Доступно {{ catalogStore.total }} квартир в режиме «Планировки».</p>
    <RouterLink :class="$style.cta" :to="link({ name: 'catalog', params: { complexId }, query: {} })">Перейти к планировкам</RouterLink>
  </section>

  <section v-else :class="$style.layout">
    <PlanViewer
      :asset="asset"
      :regions="regions"
      :selected-id="selected?.id ?? null"
      @select="onSelect"
    />

    <aside :class="$style.panel">
      <template v-if="selected">
        <h2 :class="$style.panelTitle">{{ selected.label }}</h2>
        <p :class="$style.text">Откройте корпус, чтобы выбрать этаж и квартиру на плане, или сразу перейдите к списку квартир.</p>
        <button type="button" :class="$style.cta" @click="openBuildingViz(selected)">Открыть корпус</button>
        <button type="button" :class="$style.ctaGhost" @click="openBuilding(selected)">Смотреть квартиры</button>
      </template>
      <template v-else>
        <h2 :class="$style.panelTitle">Выберите корпус</h2>
        <p :class="$style.text">Наведите и нажмите на корпус на генплане, чтобы продолжить подбор.</p>
      </template>
    </aside>
  </section>
</template>

<style module lang="scss">
.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding: 72px 32px;
  text-align: center;
  background: var(--color-surface);
  border-radius: 28px;
  box-shadow: var(--shadow-card);
}

.layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
  align-items: start;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.text {
  margin: 0;
  max-width: 460px;
  color: var(--color-text-secondary);
}

.panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 24px;
  background: var(--color-surface);
  border-radius: 24px;
  box-shadow: var(--shadow-card);
}

.panelTitle {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.cta {
  align-self: flex-start;
  padding: 12px 24px;
  font-weight: 600;
  color: var(--color-text-inverse);
  text-decoration: none;
  cursor: pointer;
  background: var(--color-primary);
  border: 0;
  border-radius: var(--radius-pill);
}

.ctaGhost {
  align-self: flex-start;
  padding: 11px 23px;
  font-weight: 600;
  color: var(--color-text-primary);
  cursor: pointer;
  background: transparent;
  border: 1px solid var(--color-surface-control);
  border-radius: var(--radius-pill);
}
</style>
