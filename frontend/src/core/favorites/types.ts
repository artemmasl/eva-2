import type { Space } from '@/core/entities/space/types';

export interface FavoriteCollection {
  id: string;
  name: string;
  createdAt: number;
}

export interface FavoriteItem {
  spaceId: string;
  addedAt: number;
  collectionIds: string[];
  space: Space;
}

export interface FavoritesState {
  version: number;
  items: FavoriteItem[];
  collections: FavoriteCollection[];
}
