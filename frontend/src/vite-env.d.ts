/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_YANDEX_MAPS_API_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare global {
  interface Window {
    ymaps?: YMaps;
  }

  // Yandex Maps JS API v2.1 is loaded at runtime; typed loosely on purpose.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  type YMaps = any;

  const ymaps: YMaps;
}

export {};
