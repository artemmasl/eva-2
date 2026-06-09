import { apiClient } from '@/core/api/client';
import type { Developer } from '@/core/entities/developer/types';
import type { ThemeConfig } from '@/core/entities/theme-config/types';

export interface DeveloperUpdate {
  name: string;
  slug: string;
  logo: string;
  phone: string;
  theme_config: ThemeConfig;
}

const authHeaders = (token: string) => ({ Authorization: `Bearer ${token}` });

export const adminApi = {
  login: (password: string) => apiClient<{ token: string }>('/api/admin/login', {
    method: 'POST',
    body: JSON.stringify({ password }),
  }),
  listDevelopers: (token: string) => apiClient<Developer[]>('/api/developers', {
    headers: authHeaders(token),
  }),
  getDeveloper: (token: string, id: string) => apiClient<Developer>(`/api/developers/${id}`, {
    headers: authHeaders(token),
  }),
  updateDeveloper: (token: string, id: string, payload: DeveloperUpdate) => apiClient<Developer>(
    `/api/developers/${id}`,
    {
      method: 'PUT',
      headers: authHeaders(token),
      body: JSON.stringify(payload),
    },
  ),
};
