<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

import BaseModal from '@/components/common/BaseModal.vue';
import type { Space } from '@/core/entities/space/types';
import { getAllCatalogSpaces } from '@/core/entities/space/use-cases';
import { useUiStore } from '@/stores/modules/ui.store';

const uiStore = useUiStore();
const router = useRouter();

const isLoading = ref(false);
const variants = ref<Space[]>([]);

const formatPrice = (amount: number): string => (
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(amount)
);

const roomsLabel = (rooms: number): string => (rooms === 0 ? 'Студия' : `${rooms}-комн.`);

const load = async (reference: Space) => {
  isLoading.value = true;

  try {
    const spaces = await getAllCatalogSpaces({
      complex_id: reference.complex_id,
      stype: 'flat',
      is_apartment: false,
      rooms: reference.rooms,
    });

    variants.value = spaces
      .filter((space) => space.id !== reference.id && Math.abs(space.area - reference.area) <= 2)
      .sort((a, b) => a.price.amount - b.price.amount);
  } finally {
    isLoading.value = false;
  }
};

watch(() => uiStore.sameLayoutSpace, (reference) => {
  variants.value = [];

  if (reference) {
    void load(reference);
  }
}, { immediate: true });

const openSpace = (space: Space) => {
  uiStore.closeSameLayout();
  void router.push({ name: 'space-details', params: { complexId: space.complex_id, id: space.id } });
};
</script>

<template>
  <BaseModal
    v-if="uiStore.isSameLayoutOpen"
    labelled-by="same-layout-title"
    :panel-class="$style.panel"
    @close="uiStore.closeSameLayout()"
  >
    <header class="flex items-center justify-between gap-4">
      <h2 id="same-layout-title" :class="$style.title">Квартиры с такой планировкой</h2>
      <button type="button" :class="$style.close" aria-label="Закрыть" @click="uiStore.closeSameLayout()">✕</button>
    </header>

    <p v-if="isLoading" :class="$style.text">Загрузка…</p>
    <p v-else-if="!variants.length" :class="$style.text">Других квартир с такой планировкой сейчас нет.</p>

    <ul v-else :class="$style.list">
      <li v-for="space in variants" :key="space.id">
        <button type="button" :class="$style.row" @click="openSpace(space)">
          <span :class="$style.rowMain">{{ roomsLabel(space.rooms) }} · {{ space.area }} м²</span>
          <span :class="$style.rowMeta">этаж {{ space.floor }} из {{ space.floors_total }}</span>
          <span :class="$style.rowPrice">{{ formatPrice(space.price.amount) }}</span>
        </button>
      </li>
    </ul>
  </BaseModal>
</template>

<style module lang="scss">
.panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 520px;
  max-height: 80vh;
  padding: 28px;
  overflow: hidden;
  background: var(--color-surface);
  border-radius: 28px;
  box-shadow: var(--shadow-modal);

  @media (max-width: 900px) {
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }
}

.title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.close {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  color: var(--color-text-secondary);
  cursor: pointer;
  background: var(--color-surface-control);
  border: 0;
  border-radius: var(--radius-pill);
}

.text {
  margin: 0;
  color: var(--color-text-secondary);
}

.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  list-style: none;
}

.row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
  width: 100%;
  padding: 16px 18px;
  text-align: left;
  cursor: pointer;
  background: var(--color-surface-control);
  border: 1px solid transparent;
  border-radius: var(--radius-control);
  transition: border-color 140ms ease;

  &:hover {
    border-color: var(--color-primary);
  }
}

.rowMain {
  font-weight: 600;
  color: var(--color-text-primary);
}

.rowMeta {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.rowPrice {
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
}
</style>
