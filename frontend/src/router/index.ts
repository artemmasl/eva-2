import { createRouter, createWebHistory } from 'vue-router';

import AdminDeveloperEditPage from '@/pages/admin/AdminDeveloperEditPage.vue';
import AdminDevelopersPage from '@/pages/admin/AdminDevelopersPage.vue';
import AdminLayout from '@/layouts/AdminLayout.vue';
import AdminLoginPage from '@/pages/admin/AdminLoginPage.vue';
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
import UiKitPage from '@/pages/UiKitPage.vue';
import { DEFAULT_DEVELOPER_SLUG } from '@/core/routing/storefront-link';
import { useAdminStore } from '@/stores/modules/admin.store';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/ui-kit',
      name: 'ui-kit',
      component: UiKitPage,
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLoginPage,
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-developers',
          component: AdminDevelopersPage,
        },
        {
          path: 'developers/:developerId',
          name: 'admin-developer-edit',
          component: AdminDeveloperEditPage,
        },
      ],
    },
    {
      path: '/',
      redirect: { name: 'complexes', params: { developer: DEFAULT_DEVELOPER_SLUG } },
    },
    {
      path: '/:developer',
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

router.beforeEach((to) => {
  if (!to.meta.requiresAdmin) {
    return true;
  }

  const adminStore = useAdminStore();

  if (!adminStore.isAuthenticated) {
    return { name: 'admin-login', query: { redirect: to.fullPath } };
  }

  return true;
});
