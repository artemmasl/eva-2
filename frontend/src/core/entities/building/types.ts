import type { Coordinates } from '@/core/value-objects/coordinates';

export interface Building {
  id: string;
  complex_id: string;
  developer_id: string;
  name: string;
  address: string;
  coordinates: Coordinates;
}
