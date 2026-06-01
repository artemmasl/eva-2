import type { Coordinates } from '@/core/value-objects/coordinates';

export interface Complex {
  id: string;
  developer_id: string;
  name: string;
  address: string;
  district: string;
  metro: string;
  metro_time: string;
  delivery_status: string;
  coordinates: Coordinates;
}

export interface RoomGroupStat {
  key: string;
  label: string;
  count: number;
  area_from: number;
  price_from: number;
}

export interface ComplexStats {
  flats_for_sale: number;
  spaces_for_sale: number;
  price_from: number | null;
  room_groups: RoomGroupStat[];
}

export interface ComplexSummary extends Complex {
  stats: ComplexStats;
}
