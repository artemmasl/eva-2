import type { LocationQueryValue } from 'vue-router';

export const CATALOG_VIEWS = {
  plans: 'plans',
  visual: 'visual',
  chess: 'chess',
} as const;

export type CatalogView = (typeof CATALOG_VIEWS)[keyof typeof CATALOG_VIEWS];

const CATALOG_VIEW_VALUES = Object.values(CATALOG_VIEWS) as CatalogView[];

/**
 * Resolve the `?view=` query param to a known catalog view.
 * Falls back to the default `plans` view for missing or unknown values.
 */
export const resolveCatalogView = (
  value: LocationQueryValue | LocationQueryValue[] | undefined,
): CatalogView => {
  const raw = Array.isArray(value) ? value[0] : value;

  return CATALOG_VIEW_VALUES.includes(raw as CatalogView)
    ? (raw as CatalogView)
    : CATALOG_VIEWS.plans;
};
