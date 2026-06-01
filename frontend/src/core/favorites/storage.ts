import type { FavoriteCollection, FavoriteItem, FavoritesState } from '@/core/favorites/types';

const STORAGE_KEY = 'eva:favorites';

/**
 * Current schema version. Bump this whenever the persisted shape changes
 * (e.g. a new field is added to FavoriteItem) and add a matching entry to
 * `migrations` that upgrades from the previous version to the new one.
 */
export const FAVORITES_VERSION = 1;

type UnknownState = Record<string, unknown>;

/**
 * Migrations upgrade a persisted state from version `N` to version `N + 1`.
 * Keep them small and additive so older data is never lost.
 *
 * Example for a future change that adds a `note` field in version 2:
 *   1: (state) => ({
 *     ...state,
 *     version: 2,
 *     items: (state.items as FavoriteItem[]).map((item) => ({ note: '', ...item })),
 *   }),
 */
const migrations: Record<number, (state: UnknownState) => UnknownState> = {};

export const createEmptyState = (): FavoritesState => ({
  version: FAVORITES_VERSION,
  items: [],
  collections: [],
});

const isObject = (value: unknown): value is UnknownState => (
  typeof value === 'object' && value !== null
);

const normalizeCollection = (value: unknown): FavoriteCollection | null => {
  if (!isObject(value) || typeof value.id !== 'string' || typeof value.name !== 'string') {
    return null;
  }

  return {
    id: value.id,
    name: value.name,
    createdAt: typeof value.createdAt === 'number' ? value.createdAt : Date.now(),
  };
};

const normalizeItem = (value: unknown): FavoriteItem | null => {
  if (!isObject(value) || typeof value.spaceId !== 'string' || !isObject(value.space)) {
    return null;
  }

  return {
    spaceId: value.spaceId,
    addedAt: typeof value.addedAt === 'number' ? value.addedAt : Date.now(),
    collectionIds: Array.isArray(value.collectionIds)
      ? value.collectionIds.filter((id): id is string => typeof id === 'string')
      : [],
    space: value.space as unknown as FavoriteItem['space'],
  };
};

/**
 * Defensive backfill: guarantees the in-memory state always has every field,
 * even if the stored payload was partial, hand-edited or from a build that
 * predates a field. Migrations handle structural changes; this handles drift.
 */
const normalizeState = (state: UnknownState): FavoritesState => {
  const items = Array.isArray(state.items)
    ? state.items.map(normalizeItem).filter((item): item is FavoriteItem => item !== null)
    : [];
  const collections = Array.isArray(state.collections)
    ? state.collections
      .map(normalizeCollection)
      .filter((collection): collection is FavoriteCollection => collection !== null)
    : [];
  const knownCollectionIds = new Set(collections.map((collection) => collection.id));

  return {
    version: FAVORITES_VERSION,
    collections,
    items: items.map((item) => ({
      ...item,
      collectionIds: item.collectionIds.filter((id) => knownCollectionIds.has(id)),
    })),
  };
};

const runMigrations = (rawState: UnknownState): UnknownState => {
  let state = rawState;
  let version = typeof state.version === 'number' ? state.version : 0;

  while (version < FAVORITES_VERSION) {
    const migrate = migrations[version];

    if (!migrate) {
      // No migration path for this version: fall back to defaults to avoid
      // corrupt reads, while normalizeState still salvages valid entries.
      return { ...createEmptyState(), items: state.items, collections: state.collections };
    }

    state = migrate(state);
    version = typeof state.version === 'number' ? state.version : version + 1;
  }

  return state;
};

export const loadFavoritesState = (): FavoritesState => {
  if (typeof window === 'undefined') {
    return createEmptyState();
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);

    if (!raw) {
      return createEmptyState();
    }

    const parsed: unknown = JSON.parse(raw);

    if (!isObject(parsed)) {
      return createEmptyState();
    }

    return normalizeState(runMigrations(parsed));
  } catch {
    return createEmptyState();
  }
};

export const saveFavoritesState = (state: FavoritesState): void => {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // Ignore quota / serialization errors — favorites are non-critical.
  }
};
