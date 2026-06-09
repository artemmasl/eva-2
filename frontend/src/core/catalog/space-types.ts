import type { SpaceFiltersMeta } from '@/core/entities/space/types';

/**
 * Whether a space-type tab/link should be shown for the current complex.
 * `flat` types are split by the `is_apartment` flag so that the "Квартиры"
 * and "Апартаменты" entries can be hidden independently. When meta is not yet
 * loaded we keep tabs visible to avoid flicker.
 */
export const isSpaceTypeAvailable = (
  meta: SpaceFiltersMeta | null,
  stype: string,
  isApartment?: boolean,
): boolean => {
  if (!meta) {
    return true;
  }

  if (stype === 'flat') {
    return isApartment ? meta.has_apartments : meta.has_flats;
  }

  return meta.stypes.includes(stype);
};
