<script setup lang="ts">
import { computed, ref } from 'vue';

import CatalogFilters from '@/components/catalog/CatalogFilters.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import { useCatalogStore } from '@/stores/modules/catalog.store';

const catalogStore = useCatalogStore();
const areFiltersExpanded = ref(false);

const activeFiltersCount = computed(() =>
  Object.entries(catalogStore.filters).filter(([key, value]) => (
    key !== 'tenant_id'
    && key !== 'stype'
    && key !== 'is_apartment'
    && value !== undefined
    && value !== null
    && value !== ''
  )).length,
);
</script>

<template>
  <div
    :class="[
      $style.filtersShell,
      areFiltersExpanded ? $style.filtersShellExpanded : $style.filtersShellCollapsed,
    ]"
  >
    <div :class="$style.filtersPanelSlot">
      <CatalogFilters
        class="w-full transform-gpu"
        :buildings="catalogStore.buildings"
        :filters="catalogStore.filters"
        :filters-meta="catalogStore.filtersMeta"
        @change="catalogStore.updateFilters"
        @collapse="areFiltersExpanded = false"
        @open-all="catalogStore.openFiltersModal"
        @reset="catalogStore.resetFilters"
      />
    </div>
    <div :class="$style.filtersToggleSlot">
      <button
        class="relative inline-flex h-7 cursor-pointer items-center justify-center gap-1.5 self-center rounded-full border-0 px-4 text-xs -my-2.5"
        :class="$style.filtersToggle"
        type="button"
        aria-label="Развернуть фильтры"
        @click="areFiltersExpanded = true"
      >
        <BaseIcon name="chevron-down" :size="12" />
        <span>Фильтры</span>
        <span v-if="activeFiltersCount > 0" class="absolute grid place-items-center rounded-full" :class="$style.filtersBadge">{{ activeFiltersCount }}</span>
      </button>
    </div>
  </div>
</template>

<style module lang="scss">
.filtersToggle {
  color: var(--color-text-inverse);
  background: var(--color-text-primary);
  margin-bottom: -34px;
}

.filtersBadge {
  right: -7px;
  bottom: -9px;
  width: 18px;
  height: 18px;
  color: var(--color-text-inverse);
  font-size: 11px;
  background: var(--color-primary);
}

.filtersShell {
  display: grid;
  width: 100%;
}

.filtersPanelSlot,
.filtersToggleSlot {
  grid-area: 1 / 1;
  will-change: max-height, opacity, transform;
}

.filtersPanelSlot {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  transition:
    max-height 520ms cubic-bezier(0.16, 1, 0.3, 1),
    opacity 360ms ease,
    transform 520ms cubic-bezier(0.16, 1, 0.3, 1);
  transform: translate3d(0, -16px, 0);
}

.filtersToggleSlot {
  display: grid;
  min-height: 28px;
  max-height: 44px;
  place-items: center;
  opacity: 1;
  overflow: visible;
  transition:
    opacity 220ms ease-out,
    transform 280ms cubic-bezier(0.16, 1, 0.3, 1);
  transform: translate3d(0, 0, 0);
}

.filtersShellExpanded {
  .filtersPanelSlot {
    max-height: 180px;
    opacity: 1;
    overflow: visible;
    pointer-events: auto;
    transform: translate3d(0, 0, 0);
  }

  .filtersToggleSlot {
    max-height: 28px;
    opacity: 0;
    pointer-events: none;
    transition: none;
    transform: translate3d(0, -10px, 0);
  }
}

.filtersShellCollapsed {
  .filtersPanelSlot {
    transition-duration: 420ms, 260ms, 420ms;
  }
}
</style>
