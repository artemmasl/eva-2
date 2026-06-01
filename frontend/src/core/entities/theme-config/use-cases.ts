import { themeConfigRepository } from '@/core/entities/theme-config/repository';
import type { ThemeConfig } from '@/core/entities/theme-config/types';

export const getThemeConfig = (tenantId: string): Promise<ThemeConfig> => themeConfigRepository.getThemeConfig(tenantId);
