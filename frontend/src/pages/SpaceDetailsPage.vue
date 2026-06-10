<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import BaseBadge from '@/components/common/BaseBadge.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import type { Space } from '@/core/entities/space/types';
import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useFavoritesStore } from '@/stores/modules/favorites.store';
import { useSpaceDetailsStore } from '@/stores/modules/space-details.store';
import { useUiStore } from '@/stores/modules/ui.store';

type StatItem = {
  label: string;
  value: string;
};

type ViewTab = {
  id: string;
  label: string;
};

type Condition = {
  text: string;
  action: boolean;
};

const route = useRoute();
const link = useStorefrontLink();
const spaceDetailsStore = useSpaceDetailsStore();
const favoritesStore = useFavoritesStore();
const uiStore = useUiStore();

const complexesTo = computed(() => link({ name: 'complexes' }));

const openSameLayout = () => {
  if (space.value) {
    uiStore.openSameLayout(space.value);
  }
};

const isFavorite = computed(() => (
  spaceDetailsStore.space ? favoritesStore.isFavorite(spaceDetailsStore.space.id) : false
));

const toggleFavorite = () => {
  if (spaceDetailsStore.space) {
    favoritesStore.toggleFavorite(spaceDetailsStore.space);
  }
};

const typeLabels: Record<string, string> = {
  parking: 'Машино-место',
  storage: 'Кладовая',
  commercial: 'Коммерческое помещение',
};

const loadCurrentSpace = () => {
  void spaceDetailsStore.loadSpace(String(route.params.id));
};

watch(() => route.params.id, loadCurrentSpace, { immediate: true });

const space = computed(() => spaceDetailsStore.space);
const isFlat = computed(() => space.value?.stype === 'flat');

const activeView = ref('plan');
const isCharsOpen = ref(true);

const viewTabs: ViewTab[] = [
  { id: 'plan', label: 'Планировка' },
  { id: 'visual', label: 'Визуализация' },
  { id: 'tour', label: '3D-тур' },
  { id: 'window', label: 'Вид из окна' },
  { id: 'floor', label: 'На этаже' },
  { id: 'map', label: 'На карте' },
];

const formatNumber = (value: number, maximumFractionDigits = 1): string => (
  new Intl.NumberFormat('ru-RU', { maximumFractionDigits }).format(value)
);

const formatPrice = (amount: number, currency = 'RUB'): string => (
  new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(amount)
);

const roomsLabel = (item: Space): string => (
  item.rooms === 0 ? 'Студия' : `${item.rooms}-комнатная`
);

const resolveTypeLabel = (item: Space): string => {
  if (item.stype === 'flat') {
    return item.is_apartment ? 'Апартаменты' : 'Квартира';
  }

  return typeLabels[item.stype] ?? 'Помещение';
};

const title = computed(() => {
  if (!space.value) {
    return '';
  }

  const area = `${formatNumber(space.value.area)} м²`;

  if (space.value.stype === 'flat') {
    return `${roomsLabel(space.value)} ${area}`;
  }

  return `${resolveTypeLabel(space.value)} ${area}`;
});

const corpNumber = computed(() => {
  if (!space.value) {
    return '';
  }

  const match = space.value.building_id.match(/\d+/);

  return match ? match[0] : space.value.building_id;
});

const subtitle = computed(() => {
  if (!space.value) {
    return '';
  }

  const current = space.value;
  const delivery = current.delivery_status === 'Сдан'
    ? 'Сдан'
    : `Сдача ${current.delivery_quarter}`;

  const parts = [delivery, `корп.${corpNumber.value}`];

  if (current.stype === 'flat') {
    parts.push(`секц. ${current.section}`);
  }

  parts.push(`этаж ${current.floor} из ${current.floors_total}`);

  return parts.join(', ');
});

const locationLine = computed(() => {
  if (!space.value) {
    return '';
  }

  return [
    space.value.building_district,
    space.value.building_metro,
    space.value.building_metro_time,
  ].filter(Boolean).join(', ');
});

const pricePerMeter = computed(() => {
  if (!space.value?.area) {
    return null;
  }

  return Math.round(space.value.price.amount / space.value.area);
});

const similarCount = computed(() => {
  if (!space.value) {
    return 0;
  }

  return ((space.value.floor + space.value.section + space.value.rooms) % 6) + 2;
});

const conditions = computed<Condition[]>(() => {
  if (!space.value) {
    return [];
  }

  if (space.value.stype === 'flat') {
    return [
      {
        text: `Ипотека от ${formatNumber(space.value.mortgage_monthly, 0)} ₽/мес, ставка от ${formatNumber(space.value.mortgage_rate)}%`,
        action: true,
      },
      {
        text: `Рассрочка без удорожания, первый взнос ${formatNumber(space.value.installment_initial, 0)} ₽`,
        action: true,
      },
      { text: '100% оплата', action: false },
    ];
  }

  return space.value.purchase_methods.map((method) => ({ text: method, action: false }));
});

const characteristics = computed<StatItem[]>(() => {
  if (!space.value) {
    return [];
  }

  const current = space.value;

  if (current.stype === 'flat') {
    return [
      { label: 'Тип', value: roomsLabel(current) },
      { label: 'Отделка', value: current.finishing || 'Без отделки' },
      { label: 'Жилая площадь', value: `${formatNumber(current.living_area)} м²` },
      { label: 'Площадь кухни', value: `${formatNumber(current.kitchen_area)} м²` },
      { label: 'Этаж', value: `${current.floor} из ${current.floors_total}` },
      { label: 'Санузлы', value: current.bathrooms ? String(current.bathrooms) : '—' },
    ];
  }

  const rows: StatItem[] = [
    { label: 'Тип', value: resolveTypeLabel(current) },
    { label: 'Площадь', value: `${formatNumber(current.area)} м²` },
    { label: current.stype === 'parking' ? 'Уровень' : 'Этаж', value: String(current.floor) },
    { label: 'Корпус', value: current.building_name },
  ];

  if (current.stype === 'commercial' && current.bathrooms) {
    rows.push({ label: 'Санузел', value: 'Есть' });
  }

  return rows;
});

const featureChips = computed(() => {
  if (!space.value) {
    return [];
  }

  return Array.from(new Set([
    ...space.value.spaces,
    ...space.value.layout_features,
    ...space.value.window_views,
  ])).filter(Boolean);
});

const highlightBadge = (badge: string): boolean => /ипотек|выгод/i.test(badge);

const galleryImages = computed(() => space.value?.images ?? []);

const fallbackMark = computed(() => {
  if (!space.value) {
    return '';
  }

  if (space.value.stype === 'flat') {
    return space.value.rooms === 0 ? 'ST' : `${space.value.rooms}К`;
  }

  const marks: Record<string, string> = {
    parking: 'P',
    storage: 'К',
    commercial: 'Б',
  };

  return marks[space.value.stype] ?? 'E';
});

const activeViewLabel = computed(() => (
  viewTabs.find((tab) => tab.id === activeView.value)?.label ?? ''
));

const requestLead = (kind: 'consultation' | 'booking' | 'conditions', title: string, description: string) => {
  uiStore.openCallback({
    kind,
    title,
    description,
    spaceId: space.value?.id ?? null,
    complexId: space.value?.complex_id ?? null,
  });
};

const shareMessage = ref('');
let shareMessageTimer: ReturnType<typeof setTimeout> | undefined;

const showShareMessage = (text: string) => {
  shareMessage.value = text;

  if (shareMessageTimer) {
    clearTimeout(shareMessageTimer);
  }

  shareMessageTimer = setTimeout(() => {
    shareMessage.value = '';
  }, 2400);
};

const shareSpace = async () => {
  const url = window.location.href;

  if (navigator.share) {
    try {
      await navigator.share({ title: title.value || document.title, url });
      return;
    } catch {
      // user cancelled or share failed — fall back to clipboard
    }
  }

  try {
    await navigator.clipboard.writeText(url);
    showShareMessage('Ссылка скопирована');
  } catch {
    showShareMessage(url);
  }
};
</script>

<template>
  <main :class="$style.content">
    <section v-if="spaceDetailsStore.isLoading" :class="$style.state">
      <span>Загружаем помещение...</span>
    </section>

    <section v-else-if="spaceDetailsStore.error" :class="$style.state">
      <h1>Помещение не найдено</h1>
      <p>{{ spaceDetailsStore.error }}</p>
      <RouterLink :class="$style.primaryLink" :to="complexesTo">Вернуться к комплексам</RouterLink>
    </section>

    <div v-else-if="space" :class="$style.layout">
      <section :class="$style.media">
        <div :class="$style.stage">
          <div :class="$style.compass" aria-hidden="true">
            <span :class="$style.compassNeedle" />
            <em>С</em>
          </div>

          <button type="button" :class="$style.fullscreen" aria-label="На весь экран">
            <BaseIcon name="expand" :size="18" />
          </button>

          <div v-if="activeView === 'map'" :class="$style.mapView">
            <span :class="$style.mapPin" />
          </div>
          <template v-else>
            <img v-if="galleryImages[0]" :class="$style.planImage" :src="galleryImages[0]" :alt="title" />
            <div v-else :class="[$style.planFallback, $style[`planFallback-${space.stype}`]]">
              <span>{{ fallbackMark }}</span>
              <small>{{ activeViewLabel }}</small>
            </div>
          </template>
        </div>

        <div :class="$style.tabs">
          <button
            v-for="tab in viewTabs"
            :key="tab.id"
            type="button"
            :class="[$style.tab, activeView === tab.id && $style.tabActive]"
            @click="activeView = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>
      </section>

      <aside :class="$style.summary">
        <div :class="$style.summaryScroll">
          <div :class="$style.summaryHead">
            <div :class="$style.headText">
              <h1>{{ title }}</h1>
              <p :class="$style.subtitle">{{ subtitle }}</p>
            </div>
            <div :class="$style.iconRail">
              <button type="button" :aria-label="isFavorite ? 'Убрать из избранного' : 'В избранное'" :aria-pressed="isFavorite" :class="isFavorite && $style.iconActive" @click="toggleFavorite">
                <BaseIcon :name="isFavorite ? 'heart-filled' : 'heart'" :size="18" />
              </button>
              <button type="button" aria-label="Поделиться" @click="shareSpace">
                <BaseIcon name="share" :size="18" />
              </button>
            </div>
          </div>

          <p v-if="shareMessage" :class="$style.shareMessage">{{ shareMessage }}</p>

          <div v-if="space.badges.length" :class="$style.badges">
            <BaseBadge
              v-for="badge in space.badges"
              :key="badge"
              :variant="highlightBadge(badge) ? 'primary' : 'neutral'"
            >{{ badge }}</BaseBadge>
            <button type="button" :class="$style.badgeMore" aria-label="Ещё метки">…</button>
          </div>

          <a v-if="locationLine" :class="$style.location" href="#" @click.prevent>{{ locationLine }}</a>

          <div :class="$style.priceRow">
            <strong>{{ formatPrice(space.price.amount, space.price.currency) }}</strong>
            <span v-if="pricePerMeter">{{ formatNumber(pricePerMeter, 0) }} ₽/м²</span>
          </div>

          <a v-if="isFlat && similarCount" :class="$style.similarLink" href="#" @click.prevent="openSameLayout">
            Ещё {{ similarCount }} квартир с такой планировкой
          </a>

          <div v-if="conditions.length" :class="$style.conditions">
            <h2 :class="$style.blockTitle">Условия покупки</h2>
            <div
              v-for="(condition, index) in conditions"
              :key="condition.text"
              :class="[$style.conditionCard, index === 0 && $style.conditionActive]"
            >
              <span>{{ condition.text }}</span>
              <button
                v-if="condition.action"
                type="button"
                :class="$style.conditionButton"
                @click="requestLead('conditions', 'Подбор условий покупки', 'Оставьте номер — менеджер подберёт условия покупки по этому помещению.')"
              >Выбрать условия</button>
            </div>
          </div>

          <button type="button" :class="$style.charsToggle" @click="isCharsOpen = !isCharsOpen">
            Все характеристики
            <BaseIcon name="chevron-down" :size="16" :class="[$style.chevron, isCharsOpen && $style.chevronOpen]" />
          </button>

          <dl v-if="isCharsOpen" :class="$style.chars">
            <div v-for="row in characteristics" :key="row.label">
              <dt>{{ row.label }}</dt>
              <dd>{{ row.value }}</dd>
            </div>
          </dl>

          <div v-if="featureChips.length" class="flex flex-wrap gap-2">
            <BaseBadge v-for="chip in featureChips" :key="chip">{{ chip }}</BaseBadge>
          </div>
        </div>

        <div :class="$style.cta">
          <button
            v-if="activeView !== 'map'"
            type="button"
            :class="$style.ctaGhost"
            @click="requestLead('consultation', 'Получить консультацию', 'Оставьте номер — менеджер ответит на вопросы по этому помещению.')"
          >Получить консультацию</button>
          <button
            type="button"
            :class="$style.ctaPrimary"
            @click="requestLead('booking', 'Забронировать помещение', 'Оставьте номер — менеджер свяжется с вами для оформления брони.')"
          >Забронировать</button>
        </div>
      </aside>
    </div>
  </main>
</template>

<style module lang="scss">
.content {
  width: 100%;
  max-width: 1328px;
  margin: 0 auto;
  padding-bottom: 32px;
  color: var(--color-text-primary);
}

.state {
  display: grid;
  min-height: 420px;
  gap: 12px;
  place-items: center;
  text-align: center;
  background: var(--color-surface);
  border-radius: 28px;
}

.primaryLink {
  color: var(--color-primary);
  text-decoration: none;
}

.layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 410px;
  align-items: start;
  gap: 16px;
}

/* ---- media ---- */
.media {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.stage {
  position: relative;
  display: grid;
  min-height: 520px;
  place-items: center;
  overflow: hidden;
  padding: 24px;
  background: var(--color-surface);
  border-radius: 28px;
  box-shadow: var(--shadow-card);
}

.compass {
  position: absolute;
  top: 22px;
  left: 22px;
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  border-radius: 50%;

  em {
    font-size: 10px;
    font-style: normal;
  }
}

.compassNeedle {
  position: absolute;
  top: 6px;
  left: 50%;
  width: 2px;
  height: 12px;
  background: var(--color-accent);
  border-radius: 2px;
  transform: translateX(-50%);
}

.fullscreen {
  position: absolute;
  top: 22px;
  right: 22px;
  display: grid;
  width: 40px;
  height: 40px;
  place-items: center;
  color: var(--color-text-secondary);
  cursor: pointer;
  background: var(--color-surface-control);
  border: 0;
  border-radius: 50%;
}

.planImage {
  width: 100%;
  height: 100%;
  max-height: 480px;
  object-fit: contain;
}

.planFallback {
  position: relative;
  display: grid;
  width: min(460px, 80%);
  aspect-ratio: 1.2;
  gap: 14px;
  place-items: center;
  align-content: center;
  color: var(--color-primary);
  background:
    linear-gradient(90deg, transparent 23%, var(--color-border) 24%, var(--color-border) 25%, transparent 26%),
    linear-gradient(90deg, transparent 62%, var(--color-border) 63%, var(--color-border) 64%, transparent 65%),
    linear-gradient(0deg, transparent 32%, var(--color-border) 33%, var(--color-border) 34%, transparent 35%),
    linear-gradient(0deg, transparent 68%, var(--color-border) 69%, var(--color-border) 70%, transparent 71%),
    var(--color-surface);
  border: 3px solid var(--color-text-primary);
  border-radius: 18px;

  span {
    display: grid;
    width: 92px;
    height: 92px;
    place-items: center;
    color: var(--color-text-inverse);
    font-size: 32px;
    font-weight: 700;
    background: var(--color-primary);
    border-radius: 50%;
  }

  small {
    color: var(--color-text-secondary);
    font-size: 13px;
  }
}

.planFallback-parking,
.planFallback-storage,
.planFallback-commercial {
  aspect-ratio: 1.65;
}

.mapView {
  display: grid;
  width: 100%;
  height: 100%;
  min-height: 472px;
  place-items: center;
  background:
    radial-gradient(circle at 30% 30%, rgba(41, 69, 255, 0.06), transparent 40%),
    repeating-linear-gradient(0deg, rgba(15, 23, 42, 0.05) 0 1px, transparent 1px 56px),
    repeating-linear-gradient(90deg, rgba(15, 23, 42, 0.05) 0 1px, transparent 1px 56px),
    #eef1f5;
  border-radius: 18px;
}

.mapPin {
  width: 20px;
  height: 20px;
  background: var(--color-primary);
  border: 4px solid var(--color-surface);
  border-radius: 50%;
  box-shadow: 0 6px 18px rgba(41, 69, 255, 0.4);
}

.tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.tab {
  height: 40px;
  padding: 0 18px;
  color: var(--color-text-primary);
  font-size: 14px;
  font-family: inherit;
  cursor: pointer;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  transition: background 0.15s ease, color 0.15s ease;
}

.tabActive {
  color: var(--color-text-inverse);
  background: var(--color-primary);
  border-color: var(--color-primary);
}

/* ---- summary ---- */
.summary {
  position: sticky;
  top: 12px;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 160px);
  background: var(--color-surface);
  border-radius: 28px;
  box-shadow: var(--shadow-card);
}

.summaryScroll {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  padding: 24px 24px 8px;
}

.summaryHead {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.headText {
  h1 {
    margin: 0 0 6px;
    font-size: 26px;
    line-height: 1.12;
  }
}

.subtitle {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.4;
}

.iconRail {
  display: flex;
  flex-direction: column;
  gap: 8px;

  button {
    display: grid;
    width: 36px;
    height: 36px;
    place-items: center;
    color: var(--color-text-secondary);
    cursor: pointer;
    background: var(--color-surface-control);
    border: 0;
    border-radius: 50%;
    transition: color 0.15s ease;

    &:hover {
      color: var(--color-primary);
    }
  }
}

.iconActive {
  color: var(--color-primary) !important;
}

.shareMessage {
  margin: -4px 0 0;
  font-size: 13px;
  color: var(--color-primary);
}

.badges {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 12px;
  color: var(--color-text-primary);
  font-size: 12px;
  background: var(--color-surface-control);
  border-radius: var(--radius-pill);
}

.badgeAccent {
  color: var(--color-text-inverse);
  background: var(--color-primary);
}

.badgeMore {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  color: var(--color-text-secondary);
  cursor: pointer;
  background: var(--color-surface-control);
  border: 0;
  border-radius: 50%;
}

.location {
  margin-top: -4px;
  color: var(--color-primary);
  font-size: 14px;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

.priceRow {
  display: flex;
  align-items: baseline;
  gap: 10px;

  strong {
    font-size: 28px;
    line-height: 1;
  }

  span {
    color: var(--color-text-secondary);
    font-size: 14px;
  }
}

.similarLink {
  margin-top: -8px;
  color: var(--color-primary);
  font-size: 14px;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

.conditions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.blockTitle {
  margin: 4px 0 0;
  font-size: 18px;
  font-weight: 600;
}

.conditionCard {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  font-size: 14px;
  line-height: 1.35;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);

  span {
    max-width: 200px;
  }
}

.conditionActive {
  border-color: var(--color-primary);
}

.conditionButton {
  flex-shrink: 0;
  height: 34px;
  padding: 0 14px;
  color: var(--color-text-inverse);
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  background: var(--color-primary);
  border: 0;
  border-radius: var(--radius-pill);
}

.charsToggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin: 4px auto 0;
  padding: 4px 8px;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-family: inherit;
  cursor: pointer;
  background: transparent;
  border: 0;
}

.chevron {
  transition: transform 0.2s ease;
}

.chevronOpen {
  transform: rotate(180deg);
}

.chars {
  display: grid;
  gap: 0;
  margin: 0;

  div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding: 12px 0;
    border-bottom: 1px solid var(--color-border);
  }

  div:last-child {
    border-bottom: 0;
  }

  dt {
    color: var(--color-text-secondary);
    font-size: 14px;
  }

  dd {
    margin: 0;
    font-size: 14px;
    font-weight: 500;
    text-align: right;
  }
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  span {
    display: inline-flex;
    align-items: center;
    min-height: 30px;
    padding: 0 12px;
    color: var(--color-text-primary);
    font-size: 13px;
    background: var(--color-surface-control);
    border-radius: var(--radius-pill);
  }
}

.cta {
  display: flex;
  gap: 10px;
  padding: 16px 24px 24px;
}

.ctaGhost,
.ctaPrimary {
  flex: 1;
  height: 48px;
  font-size: 15px;
  font-family: inherit;
  cursor: pointer;
  border-radius: var(--radius-pill);
}

.ctaGhost {
  color: var(--color-primary);
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
}

.ctaPrimary {
  color: var(--color-text-inverse);
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
}

@media (max-width: 1080px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .summary {
    position: static;
    max-height: none;
  }

  .stage {
    min-height: 420px;
  }
}

@media (max-width: 760px) {
  .content {
    padding-bottom: 12px;
  }

  .stage,
  .summary {
    border-radius: 22px;
  }

  .conditionCard span {
    max-width: none;
  }
}
</style>
