import { complexRepository } from '@/core/entities/complex/repository';
import type { ComplexSummary } from '@/core/entities/complex/types';

export const getComplexes = (): Promise<ComplexSummary[]> => complexRepository.getComplexes();

export const getComplexDetails = (id: string): Promise<ComplexSummary> => complexRepository.getComplex(id);
