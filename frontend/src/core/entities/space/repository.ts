import { spacesApi } from '@/core/api/spaces.api';
import type {
  Space,
  SpaceFilters,
  SpaceFiltersMeta,
  SpacePagination,
  SpacesPage,
} from '@/core/entities/space/types';

export const spaceRepository = {
  getSpaces: (
    filters: SpaceFilters = {},
    pagination: SpacePagination = {},
  ): Promise<SpacesPage> => spacesApi.getSpaces(filters, pagination),
  getFiltersMeta: (filters: SpaceFilters = {}): Promise<SpaceFiltersMeta> => spacesApi.getFiltersMeta(filters),
  getSpace: (id: string): Promise<Space> => spacesApi.getSpace(id),
};
