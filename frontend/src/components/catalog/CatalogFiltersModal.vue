<script setup lang="ts">
import { computed, ref, watch } from 'vue';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseButtonGroup from '@/components/common/BaseButtonGroup.vue';
import BaseDropdown from '@/components/common/BaseDropdown.vue';
import BaseModal from '@/components/common/BaseModal.vue';
import RangeSlider from '@/components/common/RangeSlider.vue';
import type { Building } from '@/core/entities/building/types';
import type { SpaceFilters, SpaceFiltersMeta } from '@/core/entities/space/types';

const props = defineProps<{
  buildings: Building[];
  filters: SpaceFilters;
  filtersMeta: SpaceFiltersMeta | null;
  resultsCount: number;
}>();

const emit = defineEmits<{
  close: [];
  apply: [filters: SpaceFilters];
}>();

const draftFilters = ref<SpaceFilters>({ ...props.filters });

watch(
  () => props.filters,
  (filters) => {
    draftFilters.value = { ...filters };
  },
  { deep: true },
);

const setDraftFilters = (filters: SpaceFilters) => {
  draftFilters.value = filters;
};

const toggleFilter = (key: keyof SpaceFilters, value: string | number | boolean) => {
  setDraftFilters({
    ...draftFilters.value,
    [key]: draftFilters.value[key] === value ? undefined : value,
  });
};

const resetDraftFilters = () => {
  draftFilters.value = {
    stype: props.filters.stype,
    is_apartment: props.filters.is_apartment,
  };
};

const applyDraftFilters = () => {
  emit('apply', draftFilters.value);
};

const isResidential = computed(() => draftFilters.value.stype === 'flat');
const residentialTitle = computed(() => (draftFilters.value.is_apartment ? 'Апартаменты' : 'Квартира'));
const areaLabel = computed(() => (isResidential.value ? 'Площадь, м²' : 'Площадь помещения, м²'));

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

const paymentModeOptions = [
  { label: 'Ежемесячный платеж', value: 'monthly' },
  { label: 'Стоимость квартиры', value: 'price' },
];

const columnClass = 'grid content-start gap-4 [&_h3]:m-0 [&_h3]:text-[16px] [&_h3]:font-normal [&_h3]:leading-none [&_p]:m-0 [&_p]:text-[11px] [&_p]:text-[#111827]';
const chipsClass = 'flex flex-wrap gap-1.5';
const modalPanelClass = 'relative w-[min(100%,1102px)] rounded-[28px] bg-white px-[64px] pb-[38px] pt-[28px] max-[900px]:max-h-[92vh] max-[900px]:overflow-auto max-[900px]:rounded-t-[28px] max-[900px]:rounded-b-none max-[900px]:px-5 max-[900px]:py-7';
</script>

<template>
  <BaseModal
    labelled-by="filters-title"
    :panel-class="modalPanelClass"
    @close="emit('close')"
  >
      <button class="absolute right-6 top-6 grid h-5 w-5 cursor-pointer place-items-center rounded-full border border-[#111827] bg-white text-[15px] leading-none text-[#111827]" type="button" aria-label="Закрыть фильтры" @click="emit('close')">×</button>
      <h2 id="filters-title" class="m-0 mb-[25px] text-center text-[24px] font-normal leading-none text-[#111827]">Все фильтры</h2>

      <div class="grid grid-cols-[1fr_1fr_1.08fr] gap-[28px] max-[900px]:grid-cols-1 max-[900px]:gap-7">
        <section :class="columnClass">
          <h3>Условия покупки</h3>
          <BaseButtonGroup
            model-value="monthly"
            :options="paymentModeOptions"
            size="sm"
          />
          <RangeSlider v-if="filtersMeta" label="" unit="" :min="filtersMeta.price.min" :max="filtersMeta.price.max" :min-value="draftFilters.price_min" :max-value="draftFilters.price_max" :step="100000" @change="setDraftFilters({ ...draftFilters, price_min: $event.min, price_max: $event.max })" />
          <div :class="chipsClass">
            <BaseButton v-for="method in filtersMeta?.purchase_methods ?? []" :key="method" size="xs" tone="muted" :active="draftFilters.purchase_method === method" @click="toggleFilter('purchase_method', method)">{{ method }}</BaseButton>
            <BaseButton v-for="promotion in filtersMeta?.promotions ?? []" :key="promotion" size="xs" tone="muted" :active="draftFilters.promotion === promotion" @click="toggleFilter('promotion', promotion)">{{ promotion }}</BaseButton>
            <BaseButton size="xs" tone="muted" :active="draftFilters.has_discount" @click="toggleFilter('has_discount', true)">Со скидкой</BaseButton>
          </div>
        </section>

        <section v-if="isResidential" :class="columnClass">
          <h3>{{ residentialTitle }}</h3>
          <RangeSlider v-if="filtersMeta" label="Этаж" :min="filtersMeta.floor.min" :max="filtersMeta.floor.max" :min-value="draftFilters.floor_min" :max-value="draftFilters.floor_max" :step="1" @change="setDraftFilters({ ...draftFilters, floor_min: $event.min, floor_max: $event.max })" />
          <div :class="chipsClass">
            <BaseButton size="xs" tone="muted" :active="draftFilters.rooms === 0" @click="toggleFilter('rooms', 0)">Студия</BaseButton>
            <BaseButton v-for="rooms in [1, 2, 3, 4]" :key="rooms" size="xs" tone="muted" :active="draftFilters.rooms === rooms" @click="toggleFilter('rooms', rooms)">{{ rooms === 4 ? '4+' : rooms }}</BaseButton>
            <BaseButton size="xs" tone="muted" :active="draftFilters.exclude_first_floor" @click="toggleFilter('exclude_first_floor', true)">Не первый</BaseButton>
            <BaseButton size="xs" tone="muted" :active="draftFilters.exclude_last_floor" @click="toggleFilter('exclude_last_floor', true)">Не последний</BaseButton>
          </div>
          <RangeSlider v-if="filtersMeta" :label="areaLabel" :min="filtersMeta.area.min" :max="filtersMeta.area.max" :min-value="draftFilters.area_min" :max-value="draftFilters.area_max" :step="1" @change="setDraftFilters({ ...draftFilters, area_min: $event.min, area_max: $event.max })" />
          <RangeSlider v-if="filtersMeta" label="Площадь кухни, м²" :min="5" :max="12" :min-value="undefined" :max-value="undefined" :step="1" />
          <p>Отделка</p>
          <div :class="chipsClass">
            <BaseButton v-for="finishing in filtersMeta?.finishing ?? []" :key="finishing" size="xs" tone="muted" :active="draftFilters.finishing === finishing" @click="toggleFilter('finishing', finishing)">{{ finishing }}</BaseButton>
          </div>
        </section>

        <section :class="columnClass">
          <h3>{{ isResidential ? 'Особенности' : 'Параметры помещения' }}</h3>
          <BaseDropdown :model-value="draftFilters.building_id ?? ''" :options="buildingOptions" placeholder="Корпус" @change="setDraftFilters({ ...draftFilters, building_id: $event || undefined })" />
          <BaseDropdown :model-value="draftFilters.delivery_status ?? ''" :options="deliveryStatusOptions" placeholder="Сдан" @change="setDraftFilters({ ...draftFilters, delivery_status: $event || undefined })" />
          <RangeSlider v-if="filtersMeta && !isResidential" :label="areaLabel" :min="filtersMeta.area.min" :max="filtersMeta.area.max" :min-value="draftFilters.area_min" :max-value="draftFilters.area_max" :step="1" @change="setDraftFilters({ ...draftFilters, area_min: $event.min, area_max: $event.max })" />
          <template v-if="isResidential">
            <p>Помещения</p>
            <div :class="chipsClass">
              <BaseButton v-for="space in filtersMeta?.spaces ?? []" :key="space" size="xs" tone="muted" :active="draftFilters.space === space" @click="toggleFilter('space', space)">{{ space }}</BaseButton>
            </div>
            <p>Вид из окна</p>
            <div :class="chipsClass">
              <BaseButton v-for="windowView in filtersMeta?.window_views ?? []" :key="windowView" size="xs" tone="muted" :active="draftFilters.window_view === windowView" @click="toggleFilter('window_view', windowView)">{{ windowView }}</BaseButton>
            </div>
            <p>Планировка</p>
            <div :class="chipsClass">
              <BaseButton v-for="feature in filtersMeta?.layout_features ?? []" :key="feature" size="xs" tone="muted" :active="draftFilters.layout_feature === feature" @click="toggleFilter('layout_feature', feature)">{{ feature }}</BaseButton>
            </div>
          </template>
        </section>
      </div>

      <div class="mt-[24px] grid grid-cols-[1fr_1fr_1.08fr] items-center gap-[28px] max-[900px]:grid-cols-1 max-[900px]:gap-3">
        <span></span>
        <BaseButton class="w-full" size="lg" active @click="applyDraftFilters">Показать {{ resultsCount }} объектов</BaseButton>
        <button class="inline-flex min-h-7 cursor-pointer items-center justify-center gap-3 justify-self-center rounded-full border-0 bg-transparent px-3.5 text-[12px] text-[#111827]" type="button" @click="resetDraftFilters">
          <span class="text-[18px] leading-none">↻</span>
          <span>Сбросить все параметры</span>
        </button>
      </div>
  </BaseModal>
</template>

