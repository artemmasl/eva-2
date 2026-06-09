<script setup lang="ts">
import { computed } from 'vue';
import type { RouteLocationRaw } from 'vue-router';

import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useTenantStore } from '@/stores/modules/tenant.store';
import { useUiStore } from '@/stores/modules/ui.store';

const uiStore = useUiStore();
const tenantStore = useTenantStore();
const link = useStorefrontLink();

const navItems = computed<{ label: string; to: RouteLocationRaw }[]>(() => [
  { label: 'Все комплексы', to: link({ name: 'complexes' }) },
  { label: 'Избранное', to: link({ name: 'favorites' }) },
]);

const developer = computed(() => tenantStore.tenant?.developer ?? null);
const developerName = computed(() => developer.value?.name ?? 'Строительная компания');
const salesPhone = computed(() => developer.value?.phone ?? '+7 (343) 364-56-59');
const salesPhoneHref = computed(() => `tel:${salesPhone.value.replace(/[^\d+]/g, '')}`);
</script>

<template>
  <Transition :enter-from-class="$style.enterFrom" :leave-to-class="$style.leaveTo">
    <div v-if="uiStore.isSideMenuOpen" class="fixed inset-0 z-[120]" :class="$style.root">
      <div class="absolute inset-0" :class="$style.overlay" @click="uiStore.closeSideMenu()" />

      <aside
        class="absolute left-0 top-0 flex h-full w-[420px] max-w-[88vw] flex-col gap-7 overflow-y-auto px-12 py-9 max-md:px-7 max-md:py-7"
        :class="$style.panel"
        role="dialog"
        aria-modal="true"
        aria-label="Меню"
      >
        <button
          class="grid h-9 w-9 shrink-0 cursor-pointer place-items-center rounded-full border-0 text-lg"
          :class="$style.closeButton"
          type="button"
          aria-label="Закрыть меню"
          @click="uiStore.closeSideMenu()"
        >
          ✕
        </button>

        <h2 class="text-2xl font-semibold leading-tight" :class="$style.title">
          {{ developerName }}
        </h2>

        <nav class="flex flex-col gap-1" :class="$style.menuNav" aria-label="Основная навигация">
          <RouterLink
            v-for="item in navItems"
            :key="item.label"
            :to="item.to"
            :class="$style.menuLink"
            @click="uiStore.closeSideMenu()"
          >
            {{ item.label }}
          </RouterLink>
        </nav>

        <section class="flex flex-col gap-1.5" :class="$style.block">
          <h3 class="mb-1 text-lg font-semibold" :class="$style.blockTitle">Отдел продаж</h3>
          <p>ул. Белинского, 169Б/1</p>
          <p>Пн-Пт: 9:00 - 20:00</p>
          <p>Сб-Вс: 10:00 - 18:00</p>
          <a :href="salesPhoneHref">{{ salesPhone }}</a>
          <a href="mailto:sales@atlasgroup.su">sales@atlasgroup.su</a>
        </section>

        <section class="flex flex-col gap-1.5" :class="$style.block">
          <h3 class="mb-1 text-lg font-semibold" :class="$style.blockTitle">
            Продажа и аренда коммерческой недвижимости
          </h3>
          <p>ул. Московская, 249</p>
          <p>ПН-ПТ: 9:00 - 18:00</p>
          <a href="tel:+79093645659">+7 (909) 364-56-59</a>
          <a href="mailto:info@atlasgroup.su">info@atlasgroup.su</a>
        </section>

        <a href="https://atlasgroup.su" class="font-medium" :class="$style.siteLink">www.atlasgroup.su</a>

        <button class="mt-1 h-12 cursor-pointer rounded-full border-0 font-medium" :class="$style.feedbackButton" type="button" @click="uiStore.openCallback()">
          Обратная связь
        </button>

        <nav class="mt-1 flex items-center gap-4" :class="$style.socials" aria-label="Социальные сети">
          <a href="#" aria-label="ВКонтакте">VK</a>
          <a href="#" aria-label="Одноклассники">OK</a>
          <a href="#" aria-label="Telegram">TG</a>
        </nav>
      </aside>
    </div>
  </Transition>
</template>

<style module lang="scss">
.root {
  transition: opacity 0.25s ease;

  &.enterFrom,
  &.leaveTo {
    opacity: 0;

    .panel {
      transform: translateX(-100%);
    }
  }
}

.overlay {
  background: rgba(17, 17, 17, 0.4);
}

.panel {
  color: var(--color-text-inverse);
  background: var(--color-primary);
  border-top-right-radius: 32px;
  border-bottom-right-radius: 32px;
  box-shadow: var(--shadow-floating);
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.closeButton {
  color: var(--color-primary);
  background: var(--color-surface);
}

.title {
  letter-spacing: -0.01em;
}

.menuNav {
  flex: 1 1 auto;
  padding: 8px 0;
  border-top: 1px solid color-mix(in srgb, var(--color-text-inverse) 18%, transparent);
  border-bottom: 1px solid color-mix(in srgb, var(--color-text-inverse) 18%, transparent);
}

.menuLink {
  padding: 14px 0;
  font-size: 22px;
  font-weight: 600;
  color: var(--color-text-inverse);
  text-decoration: none;
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.8;
  }
}

.block {
  font-size: 14px;
  line-height: 1.55;
  color: color-mix(in srgb, var(--color-text-inverse) 86%, transparent);

  a {
    color: inherit;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}

.blockTitle {
  color: var(--color-text-inverse);
}

.siteLink {
  color: var(--color-text-inverse);
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

.feedbackButton {
  color: var(--color-primary);
  background: var(--color-surface);
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.9;
  }
}

.socials {
  a {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    font-size: 13px;
    font-weight: 600;
    color: var(--color-text-inverse);
    text-decoration: none;
    background: color-mix(in srgb, var(--color-text-inverse) 18%, transparent);
    border-radius: var(--radius-pill);
    transition: background 0.2s ease;

    &:hover {
      background: color-mix(in srgb, var(--color-text-inverse) 28%, transparent);
    }
  }
}
</style>
