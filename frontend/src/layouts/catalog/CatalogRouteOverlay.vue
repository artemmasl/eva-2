<script setup lang="ts">
import CatalogFiltersModal from '@/components/catalog/CatalogFiltersModal.vue';
import { useCatalogStore } from '@/stores/modules/catalog.store';
import type { SpaceFilters } from '@/core/entities/space/types';

const catalogStore = useCatalogStore();

const applyModalFilters = (filters: SpaceFilters) => {
  catalogStore.updateFilters(filters);
  catalogStore.closeFiltersModal();
};
</script>

<template>
  <Transition name="filters-modal">
    <CatalogFiltersModal
      v-if="catalogStore.isFiltersModalOpen"
      :buildings="catalogStore.buildings"
      :filters="catalogStore.filters"
      :filters-meta="catalogStore.filtersMeta"
      :results-count="catalogStore.total"
      @apply="applyModalFilters"
      @close="catalogStore.closeFiltersModal"
    />
  </Transition>
</template>

<style scoped>
.filters-modal-leave-active {
  transition: opacity 160ms ease-out;
}

.filters-modal-leave-to {
  opacity: 0;
}
</style>
