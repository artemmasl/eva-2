import type { ThemeConfig } from '@/core/entities/theme-config/types';

const HEX_COLOR = /^#([0-9a-f]{6})$/i;

/**
 * Darken a #rrggbb hex color by a 0..1 amount. Returns the input unchanged when
 * it is not a valid 6-digit hex (so we never produce a broken CSS value).
 */
const darken = (hex: string, amount = 0.14): string => {
  const match = HEX_COLOR.exec(hex);

  if (!match) {
    return hex;
  }

  const channels = match[1].match(/.{2}/g) ?? [];
  const scaled = channels.map((channel) => {
    const value = Math.round(parseInt(channel, 16) * (1 - amount));
    const clamped = Math.max(0, Math.min(255, value));

    return clamped.toString(16).padStart(2, '0');
  });

  return `#${scaled.join('')}`;
};

/**
 * Apply a developer's theme config to the document root as CSS variable
 * overrides. Reversible/idempotent: re-applies on every tenant change.
 */
export const applyThemeConfig = (theme: ThemeConfig | null | undefined): void => {
  if (typeof document === 'undefined') {
    return;
  }

  const root = document.documentElement;

  if (theme?.primaryColor) {
    root.style.setProperty('--color-primary', theme.primaryColor);
    root.style.setProperty('--color-primary-hover', darken(theme.primaryColor));
  } else {
    root.style.removeProperty('--color-primary');
    root.style.removeProperty('--color-primary-hover');
  }

  if (theme?.typography) {
    root.style.setProperty('--app-font', `'${theme.typography}', 'Jost', sans-serif`);
  } else {
    root.style.removeProperty('--app-font');
  }
};
