import { createSpace } from '@/core/entities/space/factory';
import { spaceRepository } from '@/core/entities/space/repository';
import type {
  Space,
  SpaceFilters,
  SpaceFiltersMeta,
  SpacePagination,
  SpacesPage,
} from '@/core/entities/space/types';

export const getCatalogSpaces = async (
  filters: SpaceFilters = {},
  pagination: SpacePagination = {},
): Promise<SpacesPage> => {
  const page = await spaceRepository.getSpaces(filters, pagination);

  return {
    ...page,
    items: page.items.filter((space) => createSpace(space).isAvailable),
  };
};

const MAX_SPACES_PAGE_SIZE = 100;
const MAX_SPACES_PAGES = 50;

/**
 * Fetch every available space matching the filters by paging through the API
 * (the endpoint caps `limit` at 100). Used by views that need the full set,
 * e.g. the chess board. A hard page cap guards against runaway loops.
 */
export const getAllCatalogSpaces = async (filters: SpaceFilters = {}): Promise<Space[]> => {
  const items: Space[] = [];
  let offset = 0;

  for (let requested = 0; requested < MAX_SPACES_PAGES; requested += 1) {
    const page = await getCatalogSpaces(filters, { limit: MAX_SPACES_PAGE_SIZE, offset });
    items.push(...page.items);

    if (!page.has_more) {
      break;
    }

    offset += MAX_SPACES_PAGE_SIZE;
  }

  return items;
};

export const getSpaceDetails = (id: string): Promise<Space> => spaceRepository.getSpace(id);

export const getCatalogFiltersMeta = (): Promise<SpaceFiltersMeta> => spaceRepository.getFiltersMeta();

export const searchSpaces = (spaces: Space[], search: string): Space[] => (
  spaces.filter((space) => createSpace(space).matchesSearch(search))
);
