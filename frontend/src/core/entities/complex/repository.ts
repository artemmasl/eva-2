import { complexesApi } from '@/core/api/complexes.api';
import type { ComplexSummary } from '@/core/entities/complex/types';

export const complexRepository = {
  getComplexes: (): Promise<ComplexSummary[]> => complexesApi.getComplexes(),
  getComplex: (id: string): Promise<ComplexSummary> => complexesApi.getComplex(id),
};
