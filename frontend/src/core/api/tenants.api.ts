import { apiClient } from '@/core/api/client';
import type { Tenant } from '@/core/entities/tenant/types';

export const tenantsApi = {
  getTenantByDomain: (domain: string) => apiClient<Tenant>(`/api/tenants/by-domain?domain=${encodeURIComponent(domain)}`),
  getTenantByDeveloper: (slug: string) => apiClient<Tenant>(`/api/tenants/by-developer/${encodeURIComponent(slug)}`),
  getTenant: (id: string) => apiClient<Tenant>(`/api/tenants/${id}`),
};
