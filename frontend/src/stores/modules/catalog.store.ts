import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

import { getBuildings } from '@/core/entities/building/use-cases';
import type { Building } from '@/core/entities/building/types';
import { getCatalogFiltersMeta, getCatalogSpaces, searchSpaces } from '@/core/entities/space/use-cases';
import type { Space, SpaceFilters, SpaceFiltersMeta } from '@/core/entities/space/types';

export const useCatalogStore = defineStore('catalog', () => {
  const defaultFilters: SpaceFilters = { stype: 'flat', is_apartment: false };
  const flatOnlyFilterKeys: (keyof SpaceFilters)[] = [
    'rooms',
    'bathrooms',
    'finishing',
    'space',
    'window_view',
    'layout_feature',
    'exclude_first_floor',
    'exclude_last_floor',
  ];
  const pageSize = 24;
  const filterUpdateDelay = 350;
  const spaces = ref<Space[]>([]);
  const buildings = ref<Building[]>([]);
  const complexId = ref<string | null>(null);
  const filtersMeta = ref<SpaceFiltersMeta | null>(null);
  const filters = ref<SpaceFilters>({ ...defaultFilters });
  const search = ref('');
  const isFiltersModalOpen = ref(false);
  const isLoading = ref(false);
  const isLoadingMore = ref(false);
  const total = ref(0);
  const hasMore = ref(false);
  let requestId = 0;
  let filterUpdateTimeout: ReturnType<typeof setTimeout> | undefined;

  const visibleSpaces = computed(() => searchSpaces(spaces.value, search.value));

  const requestFilters = (): SpaceFilters => (
    complexId.value ? { ...filters.value, complex_id: complexId.value } : { ...filters.value }
  );

  const setComplexId = (nextComplexId: string | null) => {
    complexId.value = nextComplexId;
  };

  const loadSpaces = async () => {
    const currentRequestId = ++requestId;

    isLoading.value = true;

    try {
      const spacesResult = await getCatalogSpaces(requestFilters(), { limit: pageSize, offset: 0 });

      if (currentRequestId !== requestId) {
        return;
      }

      spaces.value = spacesResult.items;
      total.value = spacesResult.total;
      hasMore.value = spacesResult.has_more;
    } finally {
      if (currentRequestId === requestId) {
        isLoading.value = false;
      }
    }
  };

  const loadCatalog = async () => {
    const [buildingsResult, filtersMetaResult] = await Promise.all([
      getBuildings(),
      getCatalogFiltersMeta(),
    ]);

    buildings.value = buildingsResult;
    filtersMeta.value = filtersMetaResult;

    await loadSpaces();
  };

  const loadMoreSpaces = async () => {
    if (isLoading.value || isLoadingMore.value || !hasMore.value) {
      return;
    }

    isLoadingMore.value = true;

    try {
      const spacesResult = await getCatalogSpaces(requestFilters(), {
        limit: pageSize,
        offset: spaces.value.length,
      });

      spaces.value = [...spaces.value, ...spacesResult.items];
      total.value = spacesResult.total;
      hasMore.value = spacesResult.has_more;
    } finally {
      isLoadingMore.value = false;
    }
  };

  const normalizeFilters = (nextFilters: SpaceFilters): SpaceFilters => {
    if (nextFilters.stype === 'flat') {
      return nextFilters;
    }

    return Object.fromEntries(
      Object.entries(nextFilters).filter(([key]) => !flatOnlyFilterKeys.includes(key as keyof SpaceFilters)),
    );
  };

  const setFilters = (nextFilters: SpaceFilters) => {
    filters.value = normalizeFilters(nextFilters);
  };

  const updateFilters = (nextFilters: SpaceFilters) => {
    filters.value = normalizeFilters(nextFilters);

    if (filterUpdateTimeout) {
      clearTimeout(filterUpdateTimeout);
    }

    filterUpdateTimeout = setTimeout(() => {
      filterUpdateTimeout = undefined;
      void loadSpaces();
    }, filterUpdateDelay);
  };

  const setSearch = (nextSearch: string) => {
    search.value = nextSearch;
  };

  const openFiltersModal = () => {
    isFiltersModalOpen.value = true;
  };

  const closeFiltersModal = () => {
    isFiltersModalOpen.value = false;
  };

  const resetFilters = async () => {
    filters.value = { ...defaultFilters };

    if (filterUpdateTimeout) {
      clearTimeout(filterUpdateTimeout);
      filterUpdateTimeout = undefined;
    }

    await loadSpaces();
  };

  return {
    spaces,
    buildings,
    complexId,
    filtersMeta,
    filters,
    search,
    isFiltersModalOpen,
    isLoading,
    isLoadingMore,
    total,
    hasMore,
    visibleSpaces,
    loadCatalog,
    loadMoreSpaces,
    setFilters,
    updateFilters,
    setSearch,
    openFiltersModal,
    closeFiltersModal,
    resetFilters,
    setComplexId,
  };
});
