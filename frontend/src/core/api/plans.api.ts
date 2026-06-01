import { apiClient } from '@/core/api/client';
import type { PlanAsset, PlanAssetQuery, PlanRegion } from '@/core/entities/plan/types';

const toSearchParams = (query: PlanAssetQuery): string => {
  const params = new URLSearchParams();

  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.set(key, String(value));
    }
  });

  const search = params.toString();

  return search ? `?${search}` : '';
};

export const plansApi = {
  getPlanAssets: (query: PlanAssetQuery = {}) => (
    apiClient<PlanAsset[]>(`/api/plans/assets${toSearchParams(query)}`)
  ),
  getPlanAsset: (assetId: string) => apiClient<PlanAsset>(`/api/plans/assets/${assetId}`),
  getPlanRegions: (assetId: string) => (
    apiClient<PlanRegion[]>(`/api/plans/assets/${assetId}/regions`)
  ),
};
