<script setup lang="ts">
import { computed } from 'vue';
import type { RouteLocationRaw } from 'vue-router';

import { useFavoritesStore } from '@/stores/modules/favorites.store';
import { useUiStore } from '@/stores/modules/ui.store';

const props = withDefaults(defineProps<{
  activeStype?: string;
  isApartment?: boolean;
  showTypeTabs?: boolean;
  brandTitle?: string;
  brandTo?: RouteLocationRaw;
  brandLogo?: string;
  phone?: string;
}>(), {
  showTypeTabs: true,
  brandTitle: '',
  brandTo: '/',
  brandLogo: '',
  phone: '',
});

const brandMark = computed(() => (props.brandTitle.trim().charAt(0) || 'A').toUpperCase());

const phoneHref = computed(() => `tel:${props.phone.replace(/[^\d+]/g, '')}`);

const emit = defineEmits<{
  changeType: [filters: { stype: string; is_apartment?: boolean }];
}>();

const uiStore = useUiStore();
const favoritesStore = useFavoritesStore();

const spaceTypeOptions = [
  { label: 'Квартиры', value: 'flat', filters: { stype: 'flat', is_apartment: false } },
  { label: 'Парковки', value: 'parking', filters: { stype: 'parking' } },
  { label: 'Кладовки', value: 'storage', filters: { stype: 'storage' } },
  { label: 'Коммерция', value: 'commercial', filters: { stype: 'commercial' } },
  { label: 'Апартаменты', value: 'apartment', filters: { stype: 'flat', is_apartment: true } },
];

const isOptionActive = (option: { value: string; filters: { stype: string; is_apartment?: boolean } }) => (
  option.value === 'apartment'
    ? option.filters.stype === props.activeStype && props.isApartment === true
    : option.filters.stype === props.activeStype && option.filters.is_apartment === props.isApartment
);
</script>

<template>
  <header class="fixed left-6 right-6 top-0 z-40 flex flex-col px-8 backdrop-blur-2xl max-md:left-3 max-md:right-3 max-md:px-4" :class="$style.header">
    <div class="grid items-center gap-6 max-md:gap-3" :class="$style.inner">
      <button class="flex h-9 w-9 cursor-pointer flex-col items-center justify-center gap-[5px] rounded-full border-0" :class="$style.iconButton" type="button" aria-label="Открыть меню" @click="uiStore.openSideMenu()">
        <span :class="$style.iconLine" />
        <span :class="$style.iconLine" />
      </button>

      <RouterLink class="inline-flex items-center gap-4 whitespace-nowrap font-medium no-underline" :class="$style.brandLink" :to="props.brandTo">
        <img v-if="props.brandLogo" class="h-8 w-8 rounded-full object-cover" :src="props.brandLogo" alt="" />
        <span v-else class="grid h-8 w-8 place-items-center rounded-full uppercase" :class="$style.brandMark">{{ brandMark }}</span>
        <span v-if="props.brandTitle" class="max-md:hidden">{{ props.brandTitle }}</span>
      </RouterLink>

      <nav v-if="props.showTypeTabs" class="flex justify-center gap-2" :class="$style.nav" aria-label="Catalog navigation">
        <button
          v-for="option in spaceTypeOptions"
          :key="option.value"
          type="button"
          :class="isOptionActive(option) && $style.navLinkActive"
          @click="emit('changeType', option.filters)"
        >
          {{ option.label }}
        </button>
      </nav>

      <div class="flex items-center gap-2.5">
        <a v-if="props.phone" class="whitespace-nowrap text-sm no-underline max-md:hidden" :class="$style.phoneLink" :href="phoneHref">{{ props.phone }}</a>
        <button class="inline-flex h-9 cursor-pointer items-center gap-2 rounded-full border-0 px-5 max-md:hidden" :class="$style.aiButton" type="button">
          <span :class="$style.aiSpark" aria-hidden="true">✦</span>
          AI-помощник
        </button>
        <RouterLink class="relative grid h-9 w-9 place-items-center rounded-full border-0 no-underline" :class="$style.iconButton" to="/favorites" aria-label="Избранное">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20s-7-4.35-9.33-8.3C1.3 9.36 2.2 6.4 5 5.6c1.96-.56 3.7.5 4.6 1.7L12 9l2.4-1.7c.9-1.2 2.64-2.26 4.6-1.7 2.8.8 3.7 3.76 2.33 6.1C19 15.65 12 20 12 20z" />
          </svg>
          <span v-if="favoritesStore.totalCount > 0" class="absolute -right-1 -top-1 grid h-[18px] min-w-[18px] place-items-center rounded-full px-1 text-[11px]" :class="$style.favoriteBadge">{{ favoritesStore.totalCount }}</span>
        </RouterLink>
      </div>
    </div>

    <slot />
  </header>
</template>

<style module lang="scss">
.header {
  border-bottom-right-radius: 28px;
  border-bottom-left-radius: 28px;
  background: color-mix(in srgb, var(--color-surface) 95%, transparent);
  box-shadow: var(--shadow-header);
}

.inner {
  min-height: 72px;
  grid-template-columns: auto auto 1fr auto;

  @media (max-width: 1100px) {
    grid-template-columns: auto 1fr auto;
  }
}

.iconButton {
  color: var(--color-text-secondary);
  background: var(--color-surface-control);
}

.favoriteBadge {
  color: var(--color-text-inverse);
  background: var(--color-primary);
}

.iconLine {
  width: 16px;
  height: 2px;
  background: var(--color-text-secondary);
  border-radius: var(--radius-pill);
}

.brandLink,
.phoneLink {
  color: var(--color-text-primary);
}

.brandLink {
  font-size: 22px;
}

.brandMark {
  color: var(--color-text-inverse);
  font-size: 9px;
  background: var(--color-brand);
}

.nav {
  @media (max-width: 1100px) {
    display: none;
  }

  button {
    padding: 12px 18px;
    color: var(--color-text-primary);
    cursor: pointer;
    font-size: 14px;
    font-family: inherit;
    text-decoration: none;
    background: transparent;
    border: 0;
    border-radius: var(--radius-pill);
  }
}

.navLinkActive {
  color: var(--color-text-inverse) !important;
  background: var(--color-primary) !important;
}

.aiButton {
  font-size: 14px;
  color: var(--color-text-inverse);
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
}

.aiSpark {
  font-size: 12px;
  line-height: 1;
}
</style>
