import { buildingRepository } from '@/core/entities/building/repository';
import type { Building } from '@/core/entities/building/types';

export const getBuildings = (): Promise<Building[]> => buildingRepository.getBuildings();
