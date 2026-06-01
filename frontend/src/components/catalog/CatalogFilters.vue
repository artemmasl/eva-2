<script setup lang="ts">
import { computed } from 'vue';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseDropdown from '@/components/common/BaseDropdown.vue';
import RangeSlider from '@/components/common/RangeSlider.vue';
import type { Building } from '@/core/entities/building/types';
import type { SpaceFilters, SpaceFiltersMeta } from '@/core/entities/space/types';

const props = defineProps<{
  buildings: Building[];
  filters: SpaceFilters;
  filtersMeta: SpaceFiltersMeta | null;
}>();

const emit = defineEmits<{
  change: [filters: SpaceFilters];
  collapse: [];
  openAll: [];
  reset: [];
}>();

const toNumber = (value: string): number | undefined => (value ? Number(value) : undefined);

const updateFilter = (filters: SpaceFilters, key: keyof SpaceFilters, value: string) => {
  emit('change', {
    ...filters,
    [key]: key === 'building_id' || key === 'delivery_status' ? value || undefined : toNumber(value),
  });
};

const toggleFilter = (filters: SpaceFilters, key: keyof SpaceFilters, value: string | number | boolean) => {
  emit('change', {
    ...filters,
    [key]: filters[key] === value ? undefined : value,
  });
};

const activeFiltersCount = computed(() => (
  Object.entries(props.filters).filter(([key, value]) => (
    key !== 'stype'
    && key !== 'is_apartment'
    && value !== undefined
    && value !== null
    && value !== ''
    && value !== false
  )).length
));

const getBuildingLabel = (building: Building): string => {
  const [, number] = building.id.match(/(\d+)$/) ?? [];

  return number ? `Корпус ${number}` : building.name;
};

const buildingOptions = computed(() => props.buildings.map((building) => ({
  label: getBuildingLabel(building),
  value: building.id,
})));

const deliveryStatusOptions = computed(() => (props.filtersMeta?.delivery_statuses ?? []).map((status) => ({
  label: status,
  value: status,
})));

const isResidential = computed(() => props.filters.stype === 'flat');
const title = computed(() => (props.filters.is_apartment ? 'Подобрать апартаменты' : 'Подобрать помещение'));
</script>

<template>
  <section class="relative grid gap-3.5 px-12 pb-5" :class="$style.filters">
    <div class="text-lg font-medium" :class="$style.title">{{ title }}</div>

    <div class="flex flex-wrap items-center gap-2">
      <BaseButton
        v-if="isResidential"
        :active="filters.rooms === 0"
        @click="toggleFilter(filters, 'rooms', 0)"
      >
        Студия
      </BaseButton>
      <BaseButton
        v-if="isResidential"
        v-for="rooms in [1, 2, 3, 4]"
        :key="rooms"
        variant="circle"
        :active="filters.rooms === rooms"
        @click="toggleFilter(filters, 'rooms', rooms)"
      >
        {{ rooms === 4 ? '4+' : rooms }}
      </BaseButton>

      <RangeSlider
        v-if="filtersMeta"
        label="Цена"
        unit="₽"
        :min="filtersMeta.price.min"
        :max="filtersMeta.price.max"
        :min-value="filters.price_min"
        :max-value="filters.price_max"
        :step="100000"
        @change="emit('change', { ...filters, price_min: $event.min, price_max: $event.max })"
      />

      <RangeSlider
        v-if="filtersMeta"
        label="Площадь"
        unit="м²"
        :min="filtersMeta.area.min"
        :max="filtersMeta.area.max"
        :min-value="filters.area_min"
        :max-value="filters.area_max"
        :step="1"
        @change="emit('change', { ...filters, area_min: $event.min, area_max: $event.max })"
      />

      <BaseDropdown
        :model-value="filters.building_id ?? ''"
        :options="buildingOptions"
        placeholder="Корпус"
        @change="updateFilter(filters, 'building_id', $event)"
      />

      <BaseDropdown
        :model-value="filters.delivery_status ?? ''"
        :options="deliveryStatusOptions"
        placeholder="Сдан"
        @change="updateFilter(filters, 'delivery_status', $event)"
      />

      <BaseButton
        :active="filters.has_discount"
        @click="toggleFilter(filters, 'has_discount', true)"
      >
        Со скидкой
      </BaseButton>

      <button type="button" class="relative cursor-pointer rounded-full border-0 px-4" :class="$style.filterButton" @click="emit('openAll')">
        Все фильтры
        <span v-if="activeFiltersCount" :class="$style.filterBadge">{{ activeFiltersCount }}</span>
      </button>
    </div>

    <button type="button" class="absolute left-1/2 grid h-7 w-7 -translate-x-1/2 cursor-pointer place-items-center rounded-full border-0" :class="$style.collapseButton" aria-label="Свернуть фильтры" @click="emit('collapse')">
      <svg class="h-1.5 w-2.5 rotate-180" viewBox="0 0 10 6" aria-hidden="true">
        <path d="M4.625 5.025a.985.985 0 0 1-.231-.175L.107.563A.28.28 0 0 1 0 .35C-.004.267.032.188.107.113.182.037.257 0 .332 0s.15.037.225.113l4.337 4.337L9.232.113c.058-.059.129-.092.212-.1.083-.009.163.024.238.1.075.074.114.15.118.224.005.075-.031.15-.106.226L5.407 4.85a.984.984 0 0 1-.244.175 1.139 1.139 0 0 1-.538 0Z" fill="currentColor"/>
      </svg>
    </button>
  </section>
</template>

<style module lang="scss">
.filters {
  background: var(--color-surface);
  border-bottom-right-radius: 28px;
  border-bottom-left-radius: 28px;

  @media (max-width: 900px) {
    padding-right: 0;
    padding-bottom: 16px;
    padding-left: 0;
  }
}

.title {
  color: var(--color-text-primary);
}

.filterButton {
  height: 34px;
  color: var(--color-text-primary);
  font-size: 13px;
}

.filterButton {
  background: var(--color-surface-control);
}

.filterBadge {
  position: absolute;
  right: -5px;
  bottom: -5px;
  display: grid;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  place-items: center;
  color: var(--color-text-inverse);
  font-size: 10px;
  background: var(--color-primary);
  border-radius: 999px;
}

.filterButtonActive {
  color: var(--color-text-inverse);
  background: var(--color-primary);
}

.collapseButton {
  bottom: -14px;
  color: var(--color-text-inverse);
  background: var(--color-text-primary);
}
</style>
