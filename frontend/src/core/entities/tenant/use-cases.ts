import { tenantRepository } from '@/core/entities/tenant/repository';
import type { Tenant } from '@/core/entities/tenant/types';

export const getTenantByDomain = (domain: string): Promise<Tenant> => tenantRepository.getTenantByDomain(domain);

export const getTenantByDeveloper = (slug: string): Promise<Tenant> => tenantRepository.getTenantByDeveloper(slug);
