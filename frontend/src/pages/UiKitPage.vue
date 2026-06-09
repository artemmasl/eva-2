<script setup lang="ts">
import { ref } from 'vue';

import BaseBadge from '@/components/common/BaseBadge.vue';
import BaseButton from '@/components/common/BaseButton.vue';
import BaseButtonGroup from '@/components/common/BaseButtonGroup.vue';
import BaseCard from '@/components/common/BaseCard.vue';
import BaseCheckbox from '@/components/common/BaseCheckbox.vue';
import BaseChip from '@/components/common/BaseChip.vue';
import BaseDropdown from '@/components/common/BaseDropdown.vue';
import BaseField from '@/components/common/BaseField.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import BaseIconButton from '@/components/common/BaseIconButton.vue';
import BaseInput from '@/components/common/BaseInput.vue';
import BaseModal from '@/components/common/BaseModal.vue';
import BaseTextarea from '@/components/common/BaseTextarea.vue';
import BaseToggle from '@/components/common/BaseToggle.vue';
import RangeSlider from '@/components/common/RangeSlider.vue';

const inputValue = ref('');
const searchValue = ref('');
const phoneValue = ref('');
const textareaValue = ref('');
const checkboxValue = ref(true);
const toggleValue = ref(true);
const segmentValue = ref<string>('monthly');
const dropdownValue = ref('');
const activeChips = ref<Record<string, boolean>>({ studio: true, '1': false, '2': true });
const isModalOpen = ref(false);

const segmentOptions = [
  { label: 'Ежемесячный платёж', value: 'monthly' },
  { label: 'Стоимость', value: 'price' },
];

const dropdownOptions = [
  { label: 'Корпус 1', value: 'b1' },
  { label: 'Корпус 2', value: 'b2' },
  { label: 'Корпус 3', value: 'b3' },
];

const chipItems = [
  { key: 'studio', label: 'Студия' },
  { key: '1', label: '1' },
  { key: '2', label: '2' },
];

const toggleChip = (key: string) => {
  activeChips.value[key] = !activeChips.value[key];
};

const iconNames = [
  'heart', 'heart-filled', 'chevron-down', 'check', 'close', 'plus',
  'plus-circle', 'search', 'share', 'trash', 'file', 'expand', 'menu',
];
</script>

<template>
  <main class="mx-auto w-full max-w-[1080px] px-6 py-12">
    <header class="mb-10">
      <p class="m-0 text-sm font-medium uppercase tracking-wide text-primary">UI Kit</p>
      <h1 class="m-0 mt-1 text-[34px] font-semibold text-text-primary">Базовые компоненты</h1>
      <p class="m-0 mt-2 text-text-secondary">
        Все компоненты построены на дизайн-токенах из <code class="rounded bg-surface-control px-1.5 py-0.5 text-[13px]">tokens.scss</code>
        и автоматически перекрашиваются под тему застройщика.
      </p>
    </header>

    <div class="grid gap-7">
      <!-- Buttons -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseButton</h2>
        <div class="flex flex-wrap items-center gap-2.5">
          <BaseButton active>Primary</BaseButton>
          <BaseButton tone="light">Light</BaseButton>
          <BaseButton tone="muted">Muted</BaseButton>
          <BaseButton tone="white">White</BaseButton>
          <BaseButton tone="outline">Outline</BaseButton>
          <BaseButton tone="clear">Ghost</BaseButton>
        </div>
        <div class="flex flex-wrap items-center gap-2.5">
          <BaseButton size="sm" active>Small</BaseButton>
          <BaseButton size="md" active>Medium</BaseButton>
          <BaseButton size="lg" active>Large</BaseButton>
          <BaseButton variant="circle" active>4</BaseButton>
          <BaseButton active>
            <template #leading>
              <BaseIcon name="plus" :size="15" />
            </template>
            С иконкой
          </BaseButton>
        </div>
      </section>

      <!-- Icon buttons -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseIconButton</h2>
        <div class="flex flex-wrap items-center gap-3">
          <BaseIconButton aria-label="Избранное">
            <BaseIcon name="heart" :size="18" />
          </BaseIconButton>
          <BaseIconButton active aria-label="Активная">
            <BaseIcon name="heart-filled" :size="18" />
          </BaseIconButton>
          <BaseIconButton variant="ghost" aria-label="Закрыть">
            <BaseIcon name="close" :size="16" />
          </BaseIconButton>
          <BaseIconButton variant="primary" size="lg" aria-label="Меню">
            <BaseIcon name="menu" :size="18" />
          </BaseIconButton>
        </div>
      </section>

      <!-- Segmented + chips -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseButtonGroup (segmented) + BaseChip</h2>
        <BaseButtonGroup v-model="segmentValue" :options="segmentOptions" />
        <div class="flex flex-wrap items-center gap-2">
          <BaseChip
            v-for="chip in chipItems"
            :key="chip.key"
            :active="activeChips[chip.key]"
            @click="toggleChip(chip.key)"
          >
            {{ chip.label }}
          </BaseChip>
          <BaseChip removable @remove="() => {}">Со скидкой</BaseChip>
        </div>
        <p class="m-0 text-sm text-text-secondary">Segment: {{ segmentValue }}</p>
      </section>

      <!-- Icons -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseIcon</h2>
        <div class="flex flex-wrap gap-3">
          <div
            v-for="name in iconNames"
            :key="name"
            class="grid h-20 w-24 place-items-center gap-2 rounded-2xl border border-border text-text-primary"
          >
            <BaseIcon :name="name" :size="22" />
            <span class="text-[11px] text-text-secondary">{{ name }}</span>
          </div>
        </div>
      </section>

      <!-- Badges -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseBadge</h2>
        <div class="flex flex-wrap items-center gap-2.5">
          <BaseBadge>Neutral</BaseBadge>
          <BaseBadge variant="primary">Хит продаж</BaseBadge>
          <BaseBadge variant="info">Ипотека 6%</BaseBadge>
          <BaseBadge variant="success">Сдан</BaseBadge>
          <BaseBadge variant="sale">-15%</BaseBadge>
          <BaseBadge variant="sale" size="sm">Акция</BaseBadge>
        </div>
      </section>

      <!-- Inputs -->
      <section class="grid gap-5 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseInput / BaseTextarea / BaseField</h2>
        <div class="grid gap-5 md:grid-cols-2">
          <BaseField label="Имя" hint="Как к вам обращаться">
            <BaseInput v-model="inputValue" placeholder="Иван Иванов" />
          </BaseField>

          <BaseField label="Поиск">
            <BaseInput v-model="searchValue" type="search" placeholder="Найти помещение">
              <template #leading>
                <BaseIcon name="search" :size="16" />
              </template>
            </BaseInput>
          </BaseField>

          <BaseField label="Телефон" hint="С маской ввода">
            <BaseInput v-model="phoneValue" type="tel" mask="+7 (###) ###-##-##" placeholder="+7 (___) ___-__-__" />
          </BaseField>

          <BaseField label="Размеры">
            <BaseInput placeholder="Disabled" disabled />
          </BaseField>
        </div>

        <BaseField label="Комментарий">
          <BaseTextarea v-model="textareaValue" placeholder="Ваш вопрос менеджеру" />
        </BaseField>
      </section>

      <!-- Select / checkbox / toggle -->
      <section class="grid gap-5 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseDropdown / BaseCheckbox / BaseToggle</h2>
        <div class="flex flex-wrap items-center gap-6">
          <BaseDropdown
            v-model="dropdownValue"
            :options="dropdownOptions"
            placeholder="Корпус"
            reset-label="Любой корпус"
          />
          <BaseCheckbox v-model="checkboxValue">Только с отделкой</BaseCheckbox>
          <BaseToggle v-model="toggleValue">Показывать проданные</BaseToggle>
        </div>
      </section>

      <!-- Range -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">RangeSlider</h2>
        <RangeSlider label="Цена" unit="₽" :min="3000000" :max="25000000" :step="100000" />
      </section>

      <!-- Card + modal -->
      <section class="grid gap-4 rounded-card border border-border bg-surface p-7 shadow-card">
        <h2 class="m-0 text-lg font-medium text-text-primary">BaseCard / BaseModal</h2>
        <div class="grid gap-4 md:grid-cols-2">
          <BaseCard>
            <h3 class="m-0 text-base font-medium text-text-primary">Обычная карточка</h3>
            <p class="m-0 mt-1 text-sm text-text-secondary">Поверхность с радиусом и тенью из токенов.</p>
          </BaseCard>
          <BaseCard interactive>
            <h3 class="m-0 text-base font-medium text-text-primary">Интерактивная</h3>
            <p class="m-0 mt-1 text-sm text-text-secondary">Приподнимается при наведении.</p>
          </BaseCard>
        </div>
        <div>
          <BaseButton active @click="isModalOpen = true">Открыть модалку</BaseButton>
        </div>
      </section>
    </div>

    <BaseModal
      v-if="isModalOpen"
      panel-class="relative w-[min(100%,460px)] rounded-card bg-surface p-8 shadow-modal"
      @close="isModalOpen = false"
    >
      <h2 class="m-0 text-xl font-semibold text-text-primary">BaseModal</h2>
      <p class="m-0 mt-2 text-text-secondary">Контент модального окна. Клик по фону закрывает.</p>
      <div class="mt-5 flex justify-end gap-2.5">
        <BaseButton tone="outline" @click="isModalOpen = false">Отмена</BaseButton>
        <BaseButton active @click="isModalOpen = false">Готово</BaseButton>
      </div>
    </BaseModal>
  </main>
</template>
