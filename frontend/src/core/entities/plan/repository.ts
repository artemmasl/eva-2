import { plansApi } from '@/core/api/plans.api';
import type { PlanAsset, PlanAssetQuery, PlanRegion } from '@/core/entities/plan/types';

export const planRepository = {
  getPlanAssets: (query: PlanAssetQuery = {}): Promise<PlanAsset[]> => plansApi.getPlanAssets(query),
  getPlanAsset: (assetId: string): Promise<PlanAsset> => plansApi.getPlanAsset(assetId),
  getPlanRegions: (assetId: string): Promise<PlanRegion[]> => plansApi.getPlanRegions(assetId),
};
