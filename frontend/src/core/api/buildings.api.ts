import { apiClient } from '@/core/api/client';
import type { Building } from '@/core/entities/building/types';

export const buildingsApi = {
  getBuildings: () => apiClient<Building[]>('/api/buildings'),
};
