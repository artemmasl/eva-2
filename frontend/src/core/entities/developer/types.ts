import type { ThemeConfig } from '@/core/entities/theme-config/types';

export interface SocialLinks {
  vk: string;
  ok: string;
  telegram: string;
}

export interface Developer {
  id: string;
  name: string;
  slug: string;
  logo: string;
  phone: string;
  email: string;
  website: string;
  socials: SocialLinks;
  privacy_policy: string;
  domains: string[];
  theme_config: ThemeConfig;
}
