<script setup lang="ts">
import { computed } from 'vue';
import { Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/pagination';

import BaseBadge from '@/components/common/BaseBadge.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import type { Space } from '@/core/entities/space/types';
import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useFavoritesStore } from '@/stores/modules/favorites.store';

const props = defineProps<{
  space: Space;
}>();

const favoritesStore = useFavoritesStore();
const link = useStorefrontLink();

const isFavorite = computed(() => favoritesStore.isFavorite(props.space.id));

const detailsTo = computed(() => (
  props.space.complex_id
    ? link({ name: 'space-details', params: { complexId: props.space.complex_id, id: props.space.id } })
    : link({ name: 'complexes' })
));

const toggleFavorite = () => {
  favoritesStore.toggleFavorite(props.space);
};

const formatPrice = (amount: number, currency: string): string => (
  new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(amount)
);

const formatArea = (area: number): string => (
  new Intl.NumberFormat('ru-RU', {
    maximumFractionDigits: 1,
  }).format(area)
);

const modules = [Pagination];

const roomsLabel = computed(() => {
  if (props.space.rooms === 0) {
    return 'Студия';
  }

  if (!props.space.rooms) {
    return '';
  }

  return `${props.space.rooms}-комнатная`;
});

const typeLabel = computed(() => {
  if (props.space.stype === 'flat') {
    return props.space.is_apartment ? 'Апартаменты' : 'Квартира';
  }

  const labels: Record<string, string> = {
    parking: 'Машино-место',
    storage: 'Кладовая',
    commercial: 'Коммерция',
  };

  return labels[props.space.stype] ?? 'Помещение';
});

const cardTitle = computed(() => {
  const area = props.space.area ? `${formatArea(props.space.area)} м²` : '';

  if (props.space.stype === 'flat') {
    return [roomsLabel.value, area].filter(Boolean).join(' · ');
  }

  return [typeLabel.value, area].filter(Boolean).join(' · ');
});

const heroFallback = computed(() => {
  if (props.space.stype === 'flat') {
    return props.space.rooms === 0 ? 'ST' : `${props.space.rooms}К`;
  }

  const fallbacks: Record<string, string> = {
    parking: 'P',
    storage: 'К',
    commercial: 'Б',
  };

  return fallbacks[props.space.stype] ?? 'E';
});

const detailChips = computed(() => {
  const chips: string[] = [];

  if (props.space.stype === 'flat') {
    if (props.space.floor) {
      chips.push(`${props.space.floor} этаж`);
    }

    if (props.space.bathrooms) {
      chips.push(`${props.space.bathrooms} санузла`);
    }

    if (props.space.finishing) {
      chips.push(props.space.finishing);
    }
  } else if (props.space.stype === 'parking') {
    if (props.space.floor) {
      chips.push(`${props.space.floor} уровень`);
    }
  } else if (props.space.stype === 'storage') {
    if (props.space.floor) {
      chips.push(`${props.space.floor} этаж`);
    }
  } else if (props.space.stype === 'commercial') {
    if (props.space.floor) {
      chips.push(`${props.space.floor} этаж`);
    }

    if (props.space.bathrooms) {
      chips.push('Санузел');
    }
  }

  if (props.space.delivery_status) {
    chips.push(props.space.delivery_status);
  }

  if (props.space.status) {
    chips.push(props.space.status);
  }

  return chips;
});
</script>

<template>
  <RouterLink
    :to="detailsTo"
    class="group relative grid h-full overflow-hidden rounded-[28px] border border-[#e5e7eb] bg-white text-inherit no-underline shadow-[0_20px_60px_rgba(15,23,42,0.07)] transition-[transform,box-shadow] duration-300 ease-out hover:-translate-y-1.5 hover:shadow-[0_28px_70px_rgba(15,23,42,0.14)]"
  >
    <button
      type="button"
      class="absolute right-3.5 top-3.5 z-10 grid h-9 w-9 cursor-pointer place-items-center rounded-full border-0 bg-white/90 shadow-[0_6px_18px_rgba(15,23,42,0.18)] backdrop-blur transition-colors"
      :class="isFavorite ? 'text-[#2945ff]' : 'text-[#475569]'"
      :aria-label="isFavorite ? 'Убрать из избранного' : 'В избранное'"
      :aria-pressed="isFavorite"
      @click.prevent.stop="toggleFavorite"
    >
      <BaseIcon :name="isFavorite ? 'heart-filled' : 'heart'" :size="19" />
    </button>
    <div class="grid h-[190px] place-items-center bg-linear-to-br from-[#2563eb] to-[#111827] text-[44px] font-extrabold text-white [&_img]:h-full [&_img]:w-full [&_img]:object-cover">
      <Swiper
        v-if="space.images.length"
        class="h-full w-full"
        :modules="modules"
        :pagination="{ clickable: true }"
      >
        <SwiperSlide v-for="image in space.images" :key="image">
          <img :src="image" :alt="space.id" />
        </SwiperSlide>
      </Swiper>
      <span v-else>{{ heroFallback }}</span>
    </div>

    <div class="grid content-between gap-[18px] p-[22px]">
      <div>
        <p class="m-0 mb-1.5 text-[13px] text-[#64748b]">{{ typeLabel }} · {{ space.id }}</p>
        <h3 class="m-0 min-h-[58px] text-[22px] leading-[1.3]">{{ cardTitle || typeLabel }}</h3>
      </div>

      <div v-if="detailChips.length" class="flex min-h-[34px] flex-wrap gap-2">
        <BaseBadge v-for="chip in detailChips" :key="chip">{{ chip }}</BaseBadge>
      </div>

      <div class="flex items-center justify-between gap-4">
        <strong class="text-xl">{{ formatPrice(space.price.amount, space.price.currency) }}</strong>
      </div>

      <div v-if="space.badges.length" class="flex min-h-[26px] flex-wrap gap-2">
        <BaseBadge v-for="badge in space.badges" :key="badge" variant="info" size="sm">{{ badge }}</BaseBadge>
      </div>
    </div>
  </RouterLink>
</template>
