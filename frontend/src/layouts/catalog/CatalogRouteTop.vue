<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, type RouteLocationRaw } from 'vue-router';

import CatalogSearch from '@/components/catalog/CatalogSearch.vue';
import { CATALOG_VIEWS, resolveCatalogView, type CatalogView } from '@/core/catalog/views';
import { useCatalogStore } from '@/stores/modules/catalog.store';

const route = useRoute();
const catalogStore = useCatalogStore();

const activeView = computed(() => resolveCatalogView(route.query.view));

const spaceTypeNounForms: Record<string, [string, string, string]> = {
  flat: ['квартира', 'квартиры', 'квартир'],
  apartment: ['апартамент', 'апартамента', 'апартаментов'],
  parking: ['парковка', 'парковки', 'парковок'],
  storage: ['кладовка', 'кладовки', 'кладовок'],
  commercial: ['помещение', 'помещения', 'помещений'],
};

const pluralize = (count: number, [one, few, many]: [string, string, string]): string => {
  const mod10 = count % 10;
  const mod100 = count % 100;

  if (mod10 === 1 && mod100 !== 11) {
    return one;
  }

  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) {
    return few;
  }

  return many;
};

const totalLabel = computed(() => {
  const { stype, is_apartment: isApartment } = catalogStore.filters;
  const key = stype === 'flat' && isApartment ? 'apartment' : stype ?? 'flat';
  const forms = spaceTypeNounForms[key] ?? spaceTypeNounForms.flat;

  return `${catalogStore.total} ${pluralize(catalogStore.total, forms)}`;
});

const viewOptions: { key: CatalogView; label: string }[] = [
  { key: 'visual', label: 'Визуальный подбор' },
  { key: 'plans', label: 'Планировки' },
  { key: 'chess', label: 'Шахматка' },
];

const viewLink = (view: CatalogView): RouteLocationRaw => ({
  query: {
    ...route.query,
    view: view === CATALOG_VIEWS.plans ? undefined : view,
  },
});
</script>

<template>
  <section class="mx-auto mb-6 flex w-full items-center justify-between gap-6" :class="$style.topBar">
    <h1 class="m-0 text-xl font-medium">{{ totalLabel }}</h1>
    <div class="flex flex-wrap items-center justify-end gap-3" :class="$style.toolbar">
      <button class="h-9 cursor-pointer rounded-full border-0 px-5" :class="$style.toolbarButton" type="button">Сначала дешевые</button>
      <button class="h-9 cursor-pointer rounded-full border-0 bg-transparent px-5" :class="$style.toolbarButtonMuted" type="button">Группировать по планировке</button>
      <RouterLink
        v-for="option in viewOptions"
        :key="option.key"
        class="inline-flex h-9 cursor-pointer items-center rounded-full border-0 px-5 no-underline"
        :class="activeView === option.key ? $style.toolbarButtonActive : $style.toolbarButton"
        :to="viewLink(option.key)"
      >
        {{ option.label }}
      </RouterLink>
      <CatalogSearch v-model="catalogStore.search" />
    </div>
  </section>
</template>

<style module lang="scss">
.topBar {
  max-width: 1328px;

  @media (max-width: 900px) {
    flex-direction: column;
    align-items: stretch;
  }
}

.toolbar {
  @media (max-width: 900px) {
    flex-direction: column;
    align-items: stretch;
  }
}

.toolbarButton {
  color: var(--color-text-primary);
  background: var(--color-surface);
  box-shadow: var(--shadow-card);
}

.toolbarButtonMuted {
  color: var(--color-text-secondary);
}

.toolbarButtonActive {
  color: var(--color-text-inverse);
  background: var(--color-primary);
  box-shadow: var(--shadow-card);
}
</style>
