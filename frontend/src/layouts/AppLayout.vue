<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import AiAssistant from '@/components/catalog/AiAssistant.vue';
import CallbackModal from '@/components/catalog/CallbackModal.vue';
import CatalogContainer from '@/components/catalog/CatalogContainer.vue';
import CatalogFooter from '@/components/catalog/CatalogFooter.vue';
import CatalogHeader from '@/components/catalog/CatalogHeader.vue';
import SameLayoutModal from '@/components/catalog/SameLayoutModal.vue';
import SideMenu from '@/components/catalog/SideMenu.vue';
import { applyThemeConfig } from '@/core/theme/apply-theme';
import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useCatalogStore } from '@/stores/modules/catalog.store';
import { useComplexStore } from '@/stores/modules/complex.store';
import { useTenantStore } from '@/stores/modules/tenant.store';

const route = useRoute();
const router = useRouter();
const catalogStore = useCatalogStore();
const complexStore = useComplexStore();
const tenantStore = useTenantStore();
const link = useStorefrontLink();

const developerSlug = computed(() => String(route.params.developer ?? ''));

const COMPLEX_SCOPED_ROUTES = ['catalog', 'space-details', 'complex-landing', 'building-viz', 'floor-plan'];

const isComplexScoped = computed(() => COMPLEX_SCOPED_ROUTES.includes(String(route.name)));

const developer = computed(() => tenantStore.tenant?.developer ?? null);

const brandTitle = computed(() => {
  if (isComplexScoped.value && complexStore.current) {
    return complexStore.current.name;
  }

  return developer.value?.name ?? '';
});

const phone = computed(() => developer.value?.phone ?? '');
const brandLogo = computed(() => developer.value?.logo ?? '');

watch(
  developer,
  (current) => applyThemeConfig(current?.theme_config),
  { immediate: true },
);

const showTypeTabs = computed(() => isComplexScoped.value && route.name !== 'complex-landing');

const brandTo = computed(() => {
  const complexId = route.params.complexId;

  return isComplexScoped.value && complexId
    ? link({ name: 'complex-landing', params: { complexId: String(complexId) } })
    : link({ name: 'complexes' });
});

watch(
  developerSlug,
  (slug) => {
    if (slug) {
      void tenantStore.loadTenantBySlug(slug);
    }
  },
  { immediate: true },
);

watch(
  () => route.params.complexId,
  (complexId) => {
    if (complexId) {
      void complexStore.loadComplex(String(complexId));
    } else {
      complexStore.clearComplex();
    }
  },
  { immediate: true },
);

const activeStype = computed(() => (
  route.name === 'catalog' ? catalogStore.filters.stype : undefined
));

const isApartment = computed(() => (
  route.name === 'catalog' ? catalogStore.filters.is_apartment : undefined
));

const changeSpaceType = (typeFilters: { stype: string; is_apartment?: boolean }) => {
  const nextFilters = {
    stype: typeFilters.stype,
    is_apartment: typeFilters.is_apartment,
  };

  if (route.name === 'catalog') {
    catalogStore.updateFilters(nextFilters);

    return;
  }

  const complexId = route.params.complexId;

  if (!complexId) {
    return;
  }

  catalogStore.setFilters(nextFilters);
  void router.push(link({ name: 'catalog', params: { complexId: String(complexId) } }));
};
</script>

<template>
  <CatalogContainer>
    <template #header>
      <CatalogHeader
        :active-stype="activeStype"
        :is-apartment="isApartment"
        :show-type-tabs="showTypeTabs"
        :filters-meta="catalogStore.filtersMeta"
        :brand-title="brandTitle"
        :brand-to="brandTo"
        :brand-logo="brandLogo"
        :phone="phone"
        @change-type="changeSpaceType"
      >
        <RouterView name="header" />
      </CatalogHeader>
    </template>

    <template #top>
      <RouterView name="top" />
    </template>

    <RouterView />

    <template #footer>
      <RouterView v-slot="{ Component }" name="footer">
        <component :is="Component" v-if="Component" />
        <CatalogFooter v-else />
      </RouterView>
    </template>

    <template #overlay>
      <RouterView name="overlay" />
    </template>
  </CatalogContainer>

  <SideMenu />
  <AiAssistant />
  <CallbackModal />
  <SameLayoutModal />
</template>
