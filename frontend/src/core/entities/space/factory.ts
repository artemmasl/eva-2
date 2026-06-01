import { SpaceModel } from '@/core/entities/space/model';
import type { Space } from '@/core/entities/space/types';

export const createSpace = (space: Space): SpaceModel => new SpaceModel(space);
