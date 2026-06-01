<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { getAllCatalogSpaces } from '@/core/entities/space/use-cases';
import type { Space } from '@/core/entities/space/types';
import { useCatalogStore } from '@/stores/modules/catalog.store';

const route = useRoute();
const router = useRouter();
const catalogStore = useCatalogStore();

const isLoading = ref(false);
const spaces = ref<Space[]>([]);

const complexId = computed(() => (route.params.complexId ? String(route.params.complexId) : ''));

interface ChessRow {
  floor: number;
  cells: Space[];
}

const rows = computed<ChessRow[]>(() => {
  const byFloor = new Map<number, Space[]>();

  spaces.value.forEach((space) => {
    const cells = byFloor.get(space.floor) ?? [];
    cells.push(space);
    byFloor.set(space.floor, cells);
  });

  return [...byFloor.entries()]
    .sort((a, b) => b[0] - a[0])
    .map(([floor, cells]) => ({
      floor,
      cells: [...cells].sort((a, b) => (a.section - b.section) || a.id.localeCompare(b.id)),
    }));
});

const cellLabel = (space: Space): string => (space.rooms === 0 ? 'Ст' : `${space.rooms}к`);

const formatPrice = (amount: number): string => (
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(amount)
);

const cellTitle = (space: Space): string => (
  `${cellLabel(space)}, ${space.area} м², этаж ${space.floor}, секция ${space.section} — ${formatPrice(space.price.amount)}`
);

const load = async () => {
  if (!complexId.value) {
    spaces.value = [];
    return;
  }

  isLoading.value = true;

  try {
    spaces.value = await getAllCatalogSpaces({
      ...catalogStore.filters,
      complex_id: complexId.value,
    });
  } finally {
    isLoading.value = false;
  }
};

const openSpace = (space: Space) => {
  void router.push({ name: 'space-details', params: { complexId: complexId.value, id: space.id } });
};

onMounted(load);
watch([complexId, () => catalogStore.filters], load, { deep: true });
</script>

<template>
  <section v-if="isLoading && !spaces.length" :class="$style.placeholder">
    <p :class="$style.text">Загрузка шахматки…</p>
  </section>

  <section v-else-if="!rows.length" :class="$style.placeholder">
    <h2 :class="$style.title">Нет квартир</h2>
    <p :class="$style.text">По текущим фильтрам нет доступных квартир для шахматки.</p>
  </section>

  <section v-else :class="$style.board">
    <div v-for="row in rows" :key="row.floor" :class="$style.row">
      <span :class="$style.floorLabel">{{ row.floor }}</span>
      <div :class="$style.cells">
        <button
          v-for="space in row.cells"
          :key="space.id"
          type="button"
          :class="$style.cell"
          :title="cellTitle(space)"
          @click="openSpace(space)"
        >
          {{ cellLabel(space) }}
        </button>
      </div>
    </div>
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

.board {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 24px;
  overflow-x: auto;
  background: var(--color-surface);
  border-radius: 24px;
  box-shadow: var(--shadow-card);
}

.row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.floorLabel {
  flex: 0 0 32px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-align: right;
}

.cells {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.cell {
  width: 44px;
  height: 36px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-inverse);
  cursor: pointer;
  background: color-mix(in srgb, var(--color-primary) 82%, transparent);
  border: 0;
  border-radius: 8px;
  transition: transform 120ms ease, background 120ms ease;

  &:hover {
    transform: translateY(-2px);
    background: var(--color-primary);
  }
}
</style>
