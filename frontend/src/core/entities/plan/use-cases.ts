import { planRepository } from '@/core/entities/plan/repository';
import type {
  PlanAsset,
  PlanAssetQuery,
  PlanKind,
  PlanRegion,
} from '@/core/entities/plan/types';

export const getPlanAssets = (query: PlanAssetQuery = {}): Promise<PlanAsset[]> => (
  planRepository.getPlanAssets(query)
);

export const getPlanRegions = (assetId: string): Promise<PlanRegion[]> => (
  planRepository.getPlanRegions(assetId)
);

/**
 * Resolve a single plan asset for a complex + kind (+ optional target), then
 * load its regions. Returns null when no markup exists so callers can degrade
 * gracefully (Epic F3).
 */
export const getPlanWithRegions = async (
  query: { complex_id: string; kind: PlanKind; target_id?: string },
): Promise<{ asset: PlanAsset; regions: PlanRegion[] } | null> => {
  const assets = await planRepository.getPlanAssets(query);
  const asset = assets[0];

  if (!asset) {
    return null;
  }

  const regions = await planRepository.getPlanRegions(asset.id);

  return { asset, regions };
};
