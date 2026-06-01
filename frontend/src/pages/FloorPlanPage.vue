<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import PlanViewer from '@/components/plans/PlanViewer.vue';
import type { PlanAsset, PlanRegion } from '@/core/entities/plan/types';
import { getPlanWithRegions } from '@/core/entities/plan/use-cases';

const route = useRoute();
const router = useRouter();

const status = ref<'loading' | 'ready' | 'empty'>('loading');
const asset = ref<PlanAsset | null>(null);
const regions = ref<PlanRegion[]>([]);
const selected = ref<PlanRegion | null>(null);

const complexId = computed(() => (route.params.complexId ? String(route.params.complexId) : ''));
const floorId = computed(() => (route.params.floorId ? String(route.params.floorId) : ''));

const load = async () => {
  status.value = 'loading';
  selected.value = null;

  const result = await getPlanWithRegions({
    complex_id: complexId.value,
    kind: 'floor',
    target_id: floorId.value,
  });

  if (!result) {
    asset.value = null;
    regions.value = [];
    status.value = 'empty';
    return;
  }

  asset.value = result.asset;
  regions.value = result.regions.filter((region) => region.target_kind === 'space');
  status.value = 'ready';
};

const onSelect = (region: PlanRegion) => {
  if (region.status !== 'available') {
    return;
  }

  selected.value = region;
};

const openSpace = (region: PlanRegion) => {
  void router.push({ name: 'space-details', params: { complexId: complexId.value, id: region.target_id } });
};

onMounted(load);
watch([complexId, floorId], load);
</script>

<template>
  <main class="mx-auto flex w-full grow flex-col gap-6" :class="$style.page">
    <header class="flex items-center gap-4">
      <RouterLink :class="$style.back" :to="{ name: 'catalog', params: { complexId }, query: { view: 'visual' } }">← К генплану</RouterLink>
      <h1 class="m-0 text-2xl font-semibold">План этажа</h1>
    </header>

    <p v-if="status === 'loading'" :class="$style.state">Загрузка плана этажа…</p>

    <section v-else-if="status === 'empty'" :class="$style.state">
      <p>Для этого этажа ещё не загружен план.</p>
      <RouterLink :class="$style.cta" :to="{ name: 'catalog', params: { complexId } }">Смотреть квартиры</RouterLink>
    </section>

    <section v-else :class="$style.layout">
      <PlanViewer :asset="asset" :regions="regions" :selected-id="selected?.id ?? null" @select="onSelect" />

      <aside :class="$style.panel">
        <template v-if="selected">
          <h2 :class="$style.panelTitle">Квартира {{ selected.target_id }}</h2>
          <p :class="$style.text">Откройте карточку квартиры с подробностями и планировкой.</p>
          <button type="button" :class="$style.cta" @click="openSpace(selected)">Открыть квартиру</button>
        </template>
        <template v-else>
          <h2 :class="$style.panelTitle">Выберите квартиру</h2>
          <p :class="$style.text">Нажмите на квартиру на плане этажа, чтобы открыть её карточку.</p>
        </template>
      </aside>
    </section>
  </main>
</template>

<style module lang="scss">
.page {
  max-width: 1328px;
}

.back {
  color: var(--color-primary);
  text-decoration: none;
}

.state {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: flex-start;
  padding: 40px;
  color: var(--color-text-secondary);
  background: var(--color-surface);
  border-radius: 24px;
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

.text {
  margin: 0;
  color: var(--color-text-secondary);
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
</style>
