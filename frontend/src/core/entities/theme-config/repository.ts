import { themeApi } from '@/core/api/theme.api';
import type { ThemeConfig } from '@/core/entities/theme-config/types';

export const themeConfigRepository = {
  getThemeConfig: (tenantId: string): Promise<ThemeConfig> => themeApi.getThemeConfig(tenantId),
};
