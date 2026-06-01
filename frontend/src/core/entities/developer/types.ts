import type { ThemeConfig } from '@/core/entities/theme-config/types';

export interface Developer {
  id: string;
  name: string;
  slug: string;
  logo: string;
  phone: string;
  domains: string[];
  theme_config: ThemeConfig;
}
