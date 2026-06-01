import { defineStore } from 'pinia';
import { ref } from 'vue';

import { getTenantByDomain } from '@/core/entities/tenant/use-cases';
import type { Tenant } from '@/core/entities/tenant/types';

export const useTenantStore = defineStore('tenant', () => {
  const tenant = ref<Tenant | null>(null);
  const isLoading = ref(false);

  const loadTenant = async (domain: string) => {
    isLoading.value = true;

    try {
      tenant.value = await getTenantByDomain(domain);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    tenant,
    isLoading,
    loadTenant,
  };
});
