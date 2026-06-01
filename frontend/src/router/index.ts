import { createRouter, createWebHistory } from 'vue-router';

import AppLayout from '@/layouts/AppLayout.vue';
import CatalogRouteHeader from '@/layouts/catalog/CatalogRouteHeader.vue';
import CatalogRouteOverlay from '@/layouts/catalog/CatalogRouteOverlay.vue';
import CatalogRouteTop from '@/layouts/catalog/CatalogRouteTop.vue';
import BuildingViewPage from '@/pages/BuildingViewPage.vue';
import CatalogPage from '@/pages/CatalogPage.vue';
import ComplexesPage from '@/pages/ComplexesPage.vue';
import ComplexLandingPage from '@/pages/ComplexLandingPage.vue';
import FavoritesPage from '@/pages/FavoritesPage.vue';
import FloorPlanPage from '@/pages/FloorPlanPage.vue';
import SpaceDetailsPage from '@/pages/SpaceDetailsPage.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'complexes',
          component: ComplexesPage,
        },
        {
          path: 'favorites',
          name: 'favorites',
          component: FavoritesPage,
        },
        {
          path: 'complex/:complexId',
          name: 'complex-landing',
          component: ComplexLandingPage,
        },
        {
          path: 'complex/:complexId/spaces',
          name: 'catalog',
          components: {
            default: CatalogPage,
            header: CatalogRouteHeader,
            top: CatalogRouteTop,
            overlay: CatalogRouteOverlay,
          },
        },
        {
          path: 'complex/:complexId/spaces/:id',
          name: 'space-details',
          component: SpaceDetailsPage,
        },
        {
          path: 'complex/:complexId/building/:buildingId',
          name: 'building-viz',
          component: BuildingViewPage,
        },
        {
          path: 'complex/:complexId/floor/:floorId',
          name: 'floor-plan',
          component: FloorPlanPage,
        },
      ],
    },
  ],
});
