import { buildingsApi } from '@/core/api/buildings.api';
import type { Building } from '@/core/entities/building/types';

export const buildingRepository = {
  getBuildings: (): Promise<Building[]> => buildingsApi.getBuildings(),
};
