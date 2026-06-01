const YANDEX_MAPS_SRC = 'https://api-maps.yandex.ru/2.1/';

let loadPromise: Promise<YMaps> | null = null;

export class YandexMapsKeyMissingError extends Error {
  constructor() {
    super('VITE_YANDEX_MAPS_API_KEY is not set');
    this.name = 'YandexMapsKeyMissingError';
  }
}

export const isYandexMapsConfigured = (): boolean => (
  Boolean(import.meta.env.VITE_YANDEX_MAPS_API_KEY)
);

export const loadYandexMaps = (): Promise<YMaps> => {
  const apiKey = import.meta.env.VITE_YANDEX_MAPS_API_KEY;

  if (!apiKey) {
    return Promise.reject(new YandexMapsKeyMissingError());
  }

  if (window.ymaps) {
    return new Promise((resolve) => window.ymaps.ready(() => resolve(window.ymaps)));
  }

  if (loadPromise) {
    return loadPromise;
  }

  loadPromise = new Promise<YMaps>((resolve, reject) => {
    const script = document.createElement('script');

    script.src = `${YANDEX_MAPS_SRC}?apikey=${encodeURIComponent(apiKey)}&lang=ru_RU`;
    script.async = true;
    script.onload = () => {
      window.ymaps.ready(() => resolve(window.ymaps));
    };
    script.onerror = () => {
      loadPromise = null;
      reject(new Error('Failed to load Yandex Maps script'));
    };

    document.head.appendChild(script);
  });

  return loadPromise;
};
