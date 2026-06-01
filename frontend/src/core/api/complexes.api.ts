import { apiClient } from '@/core/api/client';
import type { ComplexSummary } from '@/core/entities/complex/types';

export const complexesApi = {
  getComplexes: () => apiClient<ComplexSummary[]>('/api/complexes'),
  getComplex: (id: string) => apiClient<ComplexSummary>(`/api/complexes/${id}`),
};
