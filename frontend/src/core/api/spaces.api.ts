import { apiClient } from '@/core/api/client';
import type {
  Space,
  SpaceFilters,
  SpaceFiltersMeta,
  SpacePagination,
  SpacesPage,
} from '@/core/entities/space/types';

const toSearchParams = (filters: SpaceFilters & SpacePagination): string => {
  const params = new URLSearchParams();

  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.set(key, String(value));
    }
  });

  const query = params.toString();

  return query ? `?${query}` : '';
};

export const spacesApi = {
  getSpaces: (filters: SpaceFilters = {}, pagination: SpacePagination = {}) => (
    apiClient<SpacesPage>(`/api/spaces${toSearchParams({ ...filters, ...pagination })}`)
  ),
  getFiltersMeta: () => apiClient<SpaceFiltersMeta>('/api/spaces/filters'),
  getSpace: (id: string) => apiClient<Space>(`/api/spaces/${id}`),
};
