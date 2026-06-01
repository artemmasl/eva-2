<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import type { ComplexSummary } from '@/core/entities/complex/types';
import { YandexMapsKeyMissingError, loadYandexMaps } from '@/core/maps/yandex';

const props = defineProps<{
  complexes: ComplexSummary[];
}>();

const router = useRouter();
const mapEl = ref<HTMLElement>();
const status = ref<'loading' | 'ready' | 'no-key' | 'error'>('loading');

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let map: any = null;

const formatPriceShort = (amount: number): string => {
  if (amount >= 1_000_000) {
    const millions = amount / 1_000_000;
    const value = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(millions);

    return `от ${value} млн ₽`;
  }

  return `от ${new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 }).format(amount)} ₽`;
};

const getCenter = (): [number, number] => {
  if (!props.complexes.length) {
    return [55.7558, 37.6173];
  }

  const sum = props.complexes.reduce(
    (acc, complex) => {
      acc.lat += complex.coordinates.lat;
      acc.lng += complex.coordinates.lng;

      return acc;
    },
    { lat: 0, lng: 0 },
  );

  return [sum.lat / props.complexes.length, sum.lng / props.complexes.length];
};

onMounted(async () => {
  try {
    const ymaps = await loadYandexMaps();

    if (!mapEl.value) {
      return;
    }

    map = new ymaps.Map(
      mapEl.value,
      {
        center: getCenter(),
        zoom: 11,
        controls: ['zoomControl', 'geolocationControl'],
      },
      { suppressMapOpenBlock: true },
    );

    props.complexes.forEach((complex) => {
      const placemark = new ymaps.Placemark(
        [complex.coordinates.lat, complex.coordinates.lng],
        {
          iconContent: complex.stats.price_from !== null
            ? formatPriceShort(complex.stats.price_from)
            : complex.name,
          hintContent: complex.name,
        },
        { preset: 'islands#blueStretchyIcon' },
      );

      placemark.events.add('click', () => {
        void router.push({ name: 'complex-landing', params: { complexId: complex.id } });
      });

      map.geoObjects.add(placemark);
    });

    status.value = 'ready';
  } catch (error) {
    status.value = error instanceof YandexMapsKeyMissingError ? 'no-key' : 'error';
  }
});

onBeforeUnmount(() => {
  map?.destroy?.();
  map = null;
});
</script>

<template>
  <div :class="$style.wrapper">
    <div ref="mapEl" :class="$style.map" />

    <div v-if="status !== 'ready'" :class="$style.overlay">
      <p v-if="status === 'loading'">Загрузка карты…</p>
      <p v-else-if="status === 'no-key'">
        Карта недоступна: не задан ключ <code>VITE_YANDEX_MAPS_API_KEY</code>.
      </p>
      <p v-else>Не удалось загрузить карту. Попробуйте обновить страницу.</p>
    </div>
  </div>
</template>

<style module lang="scss">
.wrapper {
  position: relative;
  height: 72vh;
  min-height: 420px;
  overflow: hidden;
  border-radius: 28px;
  box-shadow: var(--shadow-card);
}

.map {
  width: 100%;
  height: 100%;
}

.overlay {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 24px;
  color: var(--color-text-secondary);
  text-align: center;
  background: var(--color-surface);
}
</style>
