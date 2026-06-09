import type { Price } from '@/core/value-objects/price';

export interface Space {
  id: string;
  complex_id: string;
  complex_name: string;
  building_id: string;
  building_name: string;
  building_address: string;
  building_district: string;
  building_metro: string;
  building_metro_time: string;
  stype: string;
  is_apartment: boolean;
  rooms: number;
  area: number;
  floor: number;
  floors_total: number;
  section: number;
  bathrooms: number;
  living_area: number;
  kitchen_area: number;
  delivery_quarter: string;
  mortgage_monthly: number;
  mortgage_rate: number;
  installment_initial: number;
  price: Price;
  status: string;
  delivery_status: string;
  images: string[];
  badges: string[];
  finishing: string;
  purchase_methods: string[];
  promotions: string[];
  spaces: string[];
  window_views: string[];
  layout_features: string[];
}

export interface SpaceFilters {
  tenant_id?: string;
  complex_id?: string;
  stype?: string;
  is_apartment?: boolean;
  rooms?: number;
  price_min?: number;
  price_max?: number;
  area_min?: number;
  area_max?: number;
  building_id?: string;
  floor_min?: number;
  floor_max?: number;
  bathrooms?: number;
  finishing?: string;
  delivery_status?: string;
  has_discount?: boolean;
  purchase_method?: string;
  promotion?: string;
  space?: string;
  window_view?: string;
  layout_feature?: string;
  exclude_first_floor?: boolean;
  exclude_last_floor?: boolean;
  search?: string;
}

export interface SpacePagination {
  limit?: number;
  offset?: number;
}

export interface SpacesPage {
  items: Space[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

export interface NumberRange {
  min: number;
  max: number;
}

export interface SpaceFiltersMeta {
  stypes: string[];
  has_flats: boolean;
  has_apartments: boolean;
  price: NumberRange;
  area: NumberRange;
  floor: NumberRange;
  bathrooms: number[];
  finishing: string[];
  delivery_statuses: string[];
  purchase_methods: string[];
  promotions: string[];
  spaces: string[];
  window_views: string[];
  layout_features: string[];
}
