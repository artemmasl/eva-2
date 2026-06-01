export type PlanKind = 'masterplan' | 'building' | 'floor';

export type PlanRegionTargetKind = 'building' | 'floor' | 'space';

export interface PlanAsset {
  id: string;
  complex_id: string;
  kind: PlanKind;
  target_id: string;
  image_url: string;
  width: number;
  height: number;
}

export interface PlanRegion {
  id: string;
  asset_id: string;
  points: [number, number][];
  target_kind: PlanRegionTargetKind;
  target_id: string;
  label: string;
  status: string;
}

export interface PlanAssetQuery {
  complex_id?: string;
  kind?: PlanKind;
  target_id?: string;
}
