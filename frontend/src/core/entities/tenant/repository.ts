import { tenantsApi } from '@/core/api/tenants.api';
import type { Tenant } from '@/core/entities/tenant/types';

export const tenantRepository = {
  getTenantByDomain: (domain: string): Promise<Tenant> => tenantsApi.getTenantByDomain(domain),
  getTenant: (id: string): Promise<Tenant> => tenantsApi.getTenant(id),
};
