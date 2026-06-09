import { complexRepository } from '@/core/entities/complex/repository';
import type { ComplexSummary } from '@/core/entities/complex/types';

export const getComplexes = (developer?: string): Promise<ComplexSummary[]> => complexRepository.getComplexes(developer);

export const getComplexDetails = (id: string): Promise<ComplexSummary> => complexRepository.getComplex(id);
