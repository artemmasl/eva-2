import { useRoute } from 'vue-router';
import type { RouteLocationRaw } from 'vue-router';

/**
 * Default developer slug used when the URL has no `/:developer` segment
 * (e.g. landing on `/`). Mirrors the backend demo seed.
 */
export const DEFAULT_DEVELOPER_SLUG = 'atlas';

type NamedLocation = Extract<RouteLocationRaw, { name?: unknown }>;

/**
 * Returns a helper that injects the active developer slug (read from the URL)
 * into a named storefront route location. Keeps every internal link scoped to
 * the current developer (`/:developer/...`) without repeating the param.
 */
export const useStorefrontLink = () => {
  const route = useRoute();

  return (location: NamedLocation): RouteLocationRaw => {
    const developer = String(route.params.developer ?? '');
    const params = (location as { params?: Record<string, unknown> }).params ?? {};

    return {
      ...location,
      params: { developer, ...params },
    } as RouteLocationRaw;
  };
};
