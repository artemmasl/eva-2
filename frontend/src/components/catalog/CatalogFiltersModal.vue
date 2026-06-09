<script setup lang="ts">
import { computed, ref, watch } from 'vue';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseChip from '@/components/common/BaseChip.vue';
import BaseDropdown from '@/components/common/BaseDropdown.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import BaseIconButton from '@/components/common/BaseIconButton.vue';
import BaseModal from '@/components/common/BaseModal.vue';
import RangeSlider from '@/components/common/RangeSlider.vue';
import type { Building } from '@/core/entities/building/types';
import type { NumberRange, SpaceFilters, SpaceFiltersMeta } from '@/core/entities/space/types';

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
const areaLabel = computed(() => (isResidential.value ? 'Площадь,\u00A0м²' : 'Площадь\u00A0помещения,\u00A0м²'));

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

const purchaseMethods = computed(() => props.filtersMeta?.purchase_methods ?? []);
const promotions = computed(() => props.filtersMeta?.promotions ?? []);
const finishingOptions = computed(() => props.filtersMeta?.finishing ?? []);
const spaceOptions = computed(() => props.filtersMeta?.spaces ?? []);
const windowViewOptions = computed(() => props.filtersMeta?.window_views ?? []);
const layoutFeatureOptions = computed(() => props.filtersMeta?.layout_features ?? []);

const hasRange = (range?: NumberRange): boolean => Boolean(range) && range!.max > range!.min;
const priceAvailable = computed(() => hasRange(props.filtersMeta?.price));
const areaAvailable = computed(() => hasRange(props.filtersMeta?.area));
const floorAvailable = computed(() => hasRange(props.filtersMeta?.floor));
const hasDiscountAvailable = computed(() => promotions.value.some((value) => value.toLowerCase().includes('скидк')));

const showPurchaseColumn = computed(() => (
  priceAvailable.value
  || purchaseMethods.value.length > 0
  || promotions.value.length > 0
  || hasDiscountAvailable.value
));

const showApartmentColumn = computed(() => isResidential.value);

const showFeaturesColumn = computed(() => (
  buildingOptions.value.length > 0
  || deliveryStatusOptions.value.length > 0
  || (!isResidential.value && areaAvailable.value)
  || (isResidential.value && (
    spaceOptions.value.length > 0
    || windowViewOptions.value.length > 0
    || layoutFeatureOptions.value.length > 0
  ))
));

const columnClass = 'grid content-start gap-4 [&_h3]:m-0 [&_h3]:text-[16px] [&_h3]:font-medium [&_h3]:leading-none [&_p]:m-0 [&_p]:text-[12px] [&_p]:font-medium [&_p]:text-text-secondary';
const chipsClass = 'flex flex-wrap gap-2';
const modalPanelClass = 'relative w-[min(100%,1102px)] rounded-[28px] bg-white px-[64px] pb-[38px] pt-[28px] max-[900px]:max-h-[92vh] max-[900px]:overflow-auto max-[900px]:rounded-t-[28px] max-[900px]:rounded-b-none max-[900px]:px-5 max-[900px]:py-7';
</script>

<template>
  <BaseModal
    labelled-by="filters-title"
    :panel-class="modalPanelClass"
    @close="emit('close')"
  >
      <BaseIconButton class="absolute right-6 top-6" variant="surface" size="sm" aria-label="Закрыть фильтры" @click="emit('close')">
        <BaseIcon name="close" :size="14" />
      </BaseIconButton>
      <h2 id="filters-title" class="m-0 mb-[28px] text-center text-[24px] font-medium leading-none text-text-primary">Все фильтры</h2>

      <div class="grid gap-[36px] [grid-template-columns:repeat(auto-fit,minmax(248px,1fr))] max-[900px]:grid-cols-1 max-[900px]:gap-7">
        <section v-if="showPurchaseColumn" :class="columnClass">
          <h3>Условия покупки</h3>

          <RangeSlider v-if="priceAvailable && filtersMeta" label="Цена" unit="₽" :min="filtersMeta.price.min" :max="filtersMeta.price.max" :min-value="draftFilters.price_min" :max-value="draftFilters.price_max" :step="100000" @change="setDraftFilters({ ...draftFilters, price_min: $event.min, price_max: $event.max })" />

          <template v-if="purchaseMethods.length">
            <p>Способ покупки</p>
            <div :class="chipsClass">
              <BaseChip v-for="method in purchaseMethods" :key="method" size="sm" :active="draftFilters.purchase_method === method" @click="toggleFilter('purchase_method', method)">{{ method }}</BaseChip>
            </div>
          </template>

          <template v-if="promotions.length || hasDiscountAvailable">
            <p>Акции и скидки</p>
            <div :class="chipsClass">
              <BaseChip v-for="promotion in promotions" :key="promotion" size="sm" :active="draftFilters.promotion === promotion" @click="toggleFilter('promotion', promotion)">{{ promotion }}</BaseChip>
              <BaseChip v-if="hasDiscountAvailable" size="sm" :active="draftFilters.has_discount" @click="toggleFilter('has_discount', true)">Со скидкой</BaseChip>
            </div>
          </template>
        </section>

        <section v-if="showApartmentColumn" :class="columnClass">
          <h3>{{ residentialTitle }}</h3>

          <p>Комнатность</p>
          <div :class="chipsClass">
            <BaseChip size="sm" :active="draftFilters.rooms === 0" @click="toggleFilter('rooms', 0)">Студия</BaseChip>
            <BaseChip v-for="rooms in [1, 2, 3, 4]" :key="rooms" size="sm" :active="draftFilters.rooms === rooms" @click="toggleFilter('rooms', rooms)">{{ rooms === 4 ? '4+' : rooms }}</BaseChip>
          </div>

          <template v-if="floorAvailable && filtersMeta">
            <RangeSlider label="Этаж" :min="filtersMeta.floor.min" :max="filtersMeta.floor.max" :min-value="draftFilters.floor_min" :max-value="draftFilters.floor_max" :step="1" @change="setDraftFilters({ ...draftFilters, floor_min: $event.min, floor_max: $event.max })" />
            <div :class="chipsClass">
              <BaseChip size="sm" :active="draftFilters.exclude_first_floor" @click="toggleFilter('exclude_first_floor', true)">Не первый</BaseChip>
              <BaseChip size="sm" :active="draftFilters.exclude_last_floor" @click="toggleFilter('exclude_last_floor', true)">Не последний</BaseChip>
            </div>
          </template>

          <RangeSlider v-if="areaAvailable && filtersMeta" :label="areaLabel" :min="filtersMeta.area.min" :max="filtersMeta.area.max" :min-value="draftFilters.area_min" :max-value="draftFilters.area_max" :step="1" @change="setDraftFilters({ ...draftFilters, area_min: $event.min, area_max: $event.max })" />

          <template v-if="finishingOptions.length">
            <p>Отделка</p>
            <div :class="chipsClass">
              <BaseChip v-for="finishing in finishingOptions" :key="finishing" size="sm" :active="draftFilters.finishing === finishing" @click="toggleFilter('finishing', finishing)">{{ finishing }}</BaseChip>
            </div>
          </template>
        </section>

        <section v-if="showFeaturesColumn" :class="columnClass">
          <h3>{{ isResidential ? 'Особенности' : 'Параметры помещения' }}</h3>

          <BaseDropdown v-if="buildingOptions.length" :model-value="draftFilters.building_id ?? ''" :options="buildingOptions" placeholder="Корпус" @change="setDraftFilters({ ...draftFilters, building_id: $event || undefined })" />
          <BaseDropdown v-if="deliveryStatusOptions.length" :model-value="draftFilters.delivery_status ?? ''" :options="deliveryStatusOptions" placeholder="Срок сдачи" @change="setDraftFilters({ ...draftFilters, delivery_status: $event || undefined })" />

          <RangeSlider v-if="!isResidential && areaAvailable && filtersMeta" :label="areaLabel" :min="filtersMeta.area.min" :max="filtersMeta.area.max" :min-value="draftFilters.area_min" :max-value="draftFilters.area_max" :step="1" @change="setDraftFilters({ ...draftFilters, area_min: $event.min, area_max: $event.max })" />

          <template v-if="isResidential">
            <template v-if="spaceOptions.length">
              <p>Помещения</p>
              <div :class="chipsClass">
                <BaseChip v-for="space in spaceOptions" :key="space" size="sm" :active="draftFilters.space === space" @click="toggleFilter('space', space)">{{ space }}</BaseChip>
              </div>
            </template>

            <template v-if="windowViewOptions.length">
              <p>Вид из окна</p>
              <div :class="chipsClass">
                <BaseChip v-for="windowView in windowViewOptions" :key="windowView" size="sm" :active="draftFilters.window_view === windowView" @click="toggleFilter('window_view', windowView)">{{ windowView }}</BaseChip>
              </div>
            </template>

            <template v-if="layoutFeatureOptions.length">
              <p>Планировка</p>
              <div :class="chipsClass">
                <BaseChip v-for="feature in layoutFeatureOptions" :key="feature" size="sm" :active="draftFilters.layout_feature === feature" @click="toggleFilter('layout_feature', feature)">{{ feature }}</BaseChip>
              </div>
            </template>
          </template>
        </section>
      </div>

      <div class="mt-[32px] flex flex-wrap items-center justify-center gap-x-8 gap-y-4 max-[900px]:flex-col">
        <BaseButton class="min-w-[300px] max-w-[440px] flex-1 max-[900px]:w-full" size="lg" active @click="applyDraftFilters">Показать</BaseButton>
        <button class="inline-flex min-h-9 cursor-pointer items-center gap-2 rounded-pill border-0 bg-transparent px-2 text-[13px] text-text-secondary transition-colors hover:text-text-primary" type="button" @click="resetDraftFilters">
          <span class="text-[16px] leading-none">↻</span>
          <span>Сбросить все параметры</span>
        </button>
      </div>
  </BaseModal>
</template>

