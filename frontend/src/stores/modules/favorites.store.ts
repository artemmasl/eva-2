import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';

import type { Space } from '@/core/entities/space/types';
import { loadFavoritesState, saveFavoritesState } from '@/core/favorites/storage';
import type { FavoriteCollection, FavoriteItem } from '@/core/favorites/types';

export const GENERAL_COLLECTION_ID = '__general__';

export type FavoriteStype = 'all' | 'flat' | 'parking' | 'storage' | 'commercial';

const createId = (): string => (
  typeof crypto !== 'undefined' && 'randomUUID' in crypto
    ? crypto.randomUUID()
    : `c-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`
);

export const useFavoritesStore = defineStore('favorites', () => {
  const initialState = loadFavoritesState();

  const items = ref<FavoriteItem[]>(initialState.items);
  const collections = ref<FavoriteCollection[]>(initialState.collections);
  const activeCollectionId = ref<string>(GENERAL_COLLECTION_ID);
  const activeStype = ref<FavoriteStype>('all');

  watch(
    [items, collections],
    () => {
      saveFavoritesState({
        version: loadFavoritesState().version,
        items: items.value,
        collections: collections.value,
      });
    },
    { deep: true },
  );

  const favoriteIds = computed(() => new Set(items.value.map((item) => item.spaceId)));

  const isFavorite = (spaceId: string): boolean => favoriteIds.value.has(spaceId);

  const matchesStype = (item: FavoriteItem): boolean => (
    activeStype.value === 'all' || item.space.stype === activeStype.value
  );

  const inCollection = (item: FavoriteItem, collectionId: string): boolean => (
    collectionId === GENERAL_COLLECTION_ID || item.collectionIds.includes(collectionId)
  );

  const countForCollection = (collectionId: string): number => (
    items.value.filter((item) => matchesStype(item) && inCollection(item, collectionId)).length
  );

  const generalCount = computed(() => countForCollection(GENERAL_COLLECTION_ID));

  const visibleItems = computed(() => (
    items.value
      .filter((item) => matchesStype(item) && inCollection(item, activeCollectionId.value))
      .sort((a, b) => b.addedAt - a.addedAt)
  ));

  const addFavorite = (space: Space, collectionId?: string): void => {
    const existing = items.value.find((item) => item.spaceId === space.id);

    if (existing) {
      if (collectionId && collectionId !== GENERAL_COLLECTION_ID && !existing.collectionIds.includes(collectionId)) {
        existing.collectionIds.push(collectionId);
      }

      return;
    }

    items.value.push({
      spaceId: space.id,
      addedAt: Date.now(),
      collectionIds: collectionId && collectionId !== GENERAL_COLLECTION_ID ? [collectionId] : [],
      space,
    });
  };

  const removeFavorite = (spaceId: string): void => {
    items.value = items.value.filter((item) => item.spaceId !== spaceId);
  };

  const toggleFavorite = (space: Space): void => {
    if (isFavorite(space.id)) {
      removeFavorite(space.id);

      return;
    }

    addFavorite(space);
  };

  const toggleCollectionMembership = (spaceId: string, collectionId: string): void => {
    const item = items.value.find((entry) => entry.spaceId === spaceId);

    if (!item || collectionId === GENERAL_COLLECTION_ID) {
      return;
    }

    item.collectionIds = item.collectionIds.includes(collectionId)
      ? item.collectionIds.filter((id) => id !== collectionId)
      : [...item.collectionIds, collectionId];
  };

  const createCollection = (name: string): string | null => {
    const trimmed = name.trim();

    if (!trimmed) {
      return null;
    }

    const id = createId();

    collections.value.push({ id, name: trimmed, createdAt: Date.now() });

    return id;
  };

  const removeCollection = (collectionId: string): void => {
    if (collectionId === GENERAL_COLLECTION_ID) {
      return;
    }

    collections.value = collections.value.filter((collection) => collection.id !== collectionId);
    items.value.forEach((item) => {
      item.collectionIds = item.collectionIds.filter((id) => id !== collectionId);
    });

    if (activeCollectionId.value === collectionId) {
      activeCollectionId.value = GENERAL_COLLECTION_ID;
    }
  };

  const setActiveCollection = (collectionId: string): void => {
    activeCollectionId.value = collectionId;
  };

  const setActiveStype = (stype: FavoriteStype): void => {
    activeStype.value = stype;
  };

  const totalCount = computed(() => items.value.length);

  return {
    items,
    collections,
    activeCollectionId,
    activeStype,
    favoriteIds,
    visibleItems,
    generalCount,
    totalCount,
    isFavorite,
    countForCollection,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    toggleCollectionMembership,
    createCollection,
    removeCollection,
    setActiveCollection,
    setActiveStype,
  };
});
