import { apiClient } from '@/core/api/client';
import type { Lead, LeadCreate } from '@/core/entities/lead/types';

export const leadsApi = {
  submit: (payload: LeadCreate) => apiClient<Lead>('/api/leads', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
};
