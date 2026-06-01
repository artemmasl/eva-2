import { apiClient } from '@/core/api/client';
import type { Tenant } from '@/core/entities/tenant/types';

export const tenantsApi = {
  getTenantByDomain: (domain: string) => apiClient<Tenant>(`/api/tenants/by-domain?domain=${encodeURIComponent(domain)}`),
  getTenant: (id: string) => apiClient<Tenant>(`/api/tenants/${id}`),
};
