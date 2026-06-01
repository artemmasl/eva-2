import type { Developer } from '@/core/entities/developer/types';
import type { ThemeConfig } from '@/core/entities/theme-config/types';

export interface Tenant {
  id: string;
  developer: Developer;
  domain: string;
  theme_config: ThemeConfig;
}
