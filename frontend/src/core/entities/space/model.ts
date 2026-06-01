import type { Space } from '@/core/entities/space/types';

export class SpaceModel {
  private readonly state: Space;

  constructor(space: Space) {
    this.state = space;
  }

  get value(): Space {
    return this.state;
  }

  get isAvailable(): boolean {
    return this.state.status === 'available';
  }

  matchesSearch(search: string): boolean {
    const normalizedSearch = search.trim().toLowerCase();

    if (!normalizedSearch) {
      return true;
    }

    return [this.state.id, this.state.status, String(this.state.rooms), String(this.state.floor)]
      .some((value) => value.toLowerCase().includes(normalizedSearch));
  }
}
