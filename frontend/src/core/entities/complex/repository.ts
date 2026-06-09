import { complexesApi } from '@/core/api/complexes.api';
import type { ComplexSummary } from '@/core/entities/complex/types';

export const complexRepository = {
  getComplexes: (developer?: string): Promise<ComplexSummary[]> => complexesApi.getComplexes(developer),
  getComplex: (id: string): Promise<ComplexSummary> => complexesApi.getComplex(id),
};
