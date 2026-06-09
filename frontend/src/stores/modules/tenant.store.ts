import { defineStore } from 'pinia';
import { ref } from 'vue';

import { getTenantByDeveloper, getTenantByDomain } from '@/core/entities/tenant/use-cases';
import type { Tenant } from '@/core/entities/tenant/types';

export const useTenantStore = defineStore('tenant', () => {
  const tenant = ref<Tenant | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const loadTenant = async (domain: string) => {
    isLoading.value = true;

    try {
      tenant.value = await getTenantByDomain(domain);
    } finally {
      isLoading.value = false;
    }
  };

  const loadTenantBySlug = async (slug: string) => {
    if (tenant.value?.developer.slug === slug) {
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      tenant.value = await getTenantByDeveloper(slug);
    } catch {
      tenant.value = null;
      error.value = 'not-found';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    tenant,
    isLoading,
    error,
    loadTenant,
    loadTenantBySlug,
  };
});
