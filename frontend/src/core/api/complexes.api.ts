import { apiClient } from '@/core/api/client';
import type { ComplexSummary } from '@/core/entities/complex/types';

export const complexesApi = {
  getComplexes: (developer?: string) => apiClient<ComplexSummary[]>(
    developer ? `/api/complexes?developer=${encodeURIComponent(developer)}` : '/api/complexes',
  ),
  getComplex: (id: string) => apiClient<ComplexSummary>(`/api/complexes/${id}`),
};
