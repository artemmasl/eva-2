import { apiClient } from '@/core/api/client';
import type { ThemeConfig } from '@/core/entities/theme-config/types';

export const themeApi = {
  getThemeConfig: (tenantId: string) => apiClient<ThemeConfig>(`/api/theme/${tenantId}`),
};
