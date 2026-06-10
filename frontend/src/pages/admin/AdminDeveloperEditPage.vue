<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseField from '@/components/common/BaseField.vue';
import BaseInput from '@/components/common/BaseInput.vue';
import BaseTextarea from '@/components/common/BaseTextarea.vue';
import { adminApi, type DeveloperUpdate } from '@/core/api/admin.api';
import type { Developer } from '@/core/entities/developer/types';
import { useAdminStore } from '@/stores/modules/admin.store';

const route = useRoute();
const adminStore = useAdminStore();

const developerId = computed(() => String(route.params.developerId ?? ''));

const TYPOGRAPHY_OPTIONS = ['Jost', 'Inter', 'Roboto', 'Montserrat', 'Open Sans'];
const CARD_STYLE_OPTIONS = [
  { value: 'default', label: 'Стандартные карточки' },
  { value: 'flat', label: 'Плоские карточки' },
  { value: 'bordered', label: 'С обводкой' },
];

const status = ref<'loading' | 'ready' | 'error'>('loading');
const isSaving = ref(false);
const savedAt = ref<number | null>(null);
const errorText = ref<string | null>(null);

const developer = ref<Developer | null>(null);

const form = reactive<DeveloperUpdate>({
  name: '',
  slug: '',
  logo: '',
  phone: '',
  email: '',
  website: '',
  socials: {
    vk: '',
    ok: '',
    telegram: '',
  },
  privacy_policy: '',
  theme_config: {
    primaryColor: '#1f6feb',
    logo: '',
    typography: 'Jost',
    cardStyle: 'default',
  },
});

const applyToForm = (data: Developer) => {
  form.name = data.name;
  form.slug = data.slug;
  form.logo = data.logo;
  form.phone = data.phone;
  form.email = data.email;
  form.website = data.website;
  form.socials = { ...data.socials };
  form.privacy_policy = data.privacy_policy;
  form.theme_config = { ...data.theme_config };
};

onMounted(async () => {
  if (!adminStore.token) {
    return;
  }

  status.value = 'loading';

  try {
    const data = await adminApi.getDeveloper(adminStore.token, developerId.value);
    developer.value = data;
    applyToForm(data);
    status.value = 'ready';
  } catch {
    status.value = 'error';
  }
});

const save = async () => {
  if (!adminStore.token) {
    return;
  }

  errorText.value = null;
  isSaving.value = true;

  try {
    const updated = await adminApi.updateDeveloper(adminStore.token, developerId.value, {
      name: form.name,
      slug: form.slug,
      logo: form.logo,
      phone: form.phone,
      email: form.email,
      website: form.website,
      socials: { ...form.socials },
      privacy_policy: form.privacy_policy,
      theme_config: { ...form.theme_config },
    });

    developer.value = updated;
    applyToForm(updated);
    savedAt.value = Date.now();
  } catch {
    errorText.value = 'Не удалось сохранить изменения';
  } finally {
    isSaving.value = false;
  }
};

const previewStyle = computed(() => ({
  '--preview-primary': form.theme_config.primaryColor,
  fontFamily: `'${form.theme_config.typography}', sans-serif`,
}));
</script>

<template>
  <section class="flex flex-col gap-6">
    <div class="flex items-center gap-3 text-sm">
      <RouterLink :to="{ name: 'admin-developers' }" class="text-text-secondary no-underline hover:text-text-primary">
        ← Все застройщики
      </RouterLink>
    </div>

    <p v-if="status === 'loading'" class="text-sm text-text-secondary">Загрузка…</p>
    <p v-else-if="status === 'error'" class="text-sm text-accent">Застройщик не найден</p>

    <template v-else>
      <header class="flex flex-wrap items-center justify-between gap-4">
        <h1 class="m-0 text-2xl font-semibold text-text-primary">{{ developer?.name }}</h1>
        <RouterLink
          :to="{ name: 'complexes', params: { developer: form.slug } }"
          target="_blank"
          class="text-sm text-primary no-underline hover:underline"
        >
          Открыть витрину ↗
        </RouterLink>
      </header>

      <div class="grid grid-cols-[1.4fr_1fr] gap-6 max-[860px]:grid-cols-1">
        <form class="flex flex-col gap-6" @submit.prevent="save">
          <div class="flex flex-col gap-5 rounded-card bg-surface p-6 shadow-card">
            <h2 class="m-0 text-base font-semibold text-text-primary">Базовая информация</h2>

            <BaseField label="Название" html-for="dev-name">
              <BaseInput id="dev-name" v-model="form.name" tone="surface" placeholder="Название компании" />
            </BaseField>

            <BaseField label="Идентификатор (slug)" hint="Используется в адресе витрины: /slug" html-for="dev-slug">
              <BaseInput id="dev-slug" v-model="form.slug" tone="surface" placeholder="atlas" />
            </BaseField>

            <BaseField label="Телефон" html-for="dev-phone">
              <BaseInput id="dev-phone" v-model="form.phone" tone="surface" placeholder="+7 (___) ___-__-__" />
            </BaseField>

            <BaseField label="Email" html-for="dev-email">
              <BaseInput id="dev-email" v-model="form.email" tone="surface" type="email" placeholder="help@example.com" />
            </BaseField>

            <BaseField label="Сайт (URL)" html-for="dev-website">
              <BaseInput id="dev-website" v-model="form.website" tone="surface" placeholder="https://…" />
            </BaseField>

            <BaseField label="Логотип (URL)" hint="Ссылка на изображение логотипа" html-for="dev-logo">
              <BaseInput id="dev-logo" v-model="form.logo" tone="surface" placeholder="https://…" />
            </BaseField>
          </div>

          <div class="flex flex-col gap-5 rounded-card bg-surface p-6 shadow-card">
            <h2 class="m-0 text-base font-semibold text-text-primary">Соцсети</h2>

            <BaseField label="ВКонтакте" html-for="dev-vk">
              <BaseInput id="dev-vk" v-model="form.socials.vk" tone="surface" placeholder="https://vk.com/…" />
            </BaseField>

            <BaseField label="Одноклассники" html-for="dev-ok">
              <BaseInput id="dev-ok" v-model="form.socials.ok" tone="surface" placeholder="https://ok.ru/…" />
            </BaseField>

            <BaseField label="Telegram" html-for="dev-tg">
              <BaseInput id="dev-tg" v-model="form.socials.telegram" tone="surface" placeholder="https://t.me/…" />
            </BaseField>
          </div>

          <div class="flex flex-col gap-5 rounded-card bg-surface p-6 shadow-card">
            <h2 class="m-0 text-base font-semibold text-text-primary">Политика конфиденциальности</h2>

            <BaseField label="Текст политики" hint="Отображается на отдельной странице витрины" html-for="dev-privacy">
              <BaseTextarea id="dev-privacy" v-model="form.privacy_policy" :rows="10" placeholder="Текст политики конфиденциальности…" />
            </BaseField>
          </div>

          <div class="flex flex-col gap-5 rounded-card bg-surface p-6 shadow-card">
            <h2 class="m-0 text-base font-semibold text-text-primary">Глобальные стили</h2>

            <BaseField label="Основной цвет" html-for="dev-color">
              <div class="flex items-center gap-3">
                <input
                  id="dev-color"
                  v-model="form.theme_config.primaryColor"
                  type="color"
                  class="h-11 w-14 cursor-pointer rounded-control border border-border bg-surface p-1"
                />
                <BaseInput v-model="form.theme_config.primaryColor" tone="surface" placeholder="#1f6feb" />
              </div>
            </BaseField>

            <BaseField label="Шрифт" html-for="dev-font">
              <select
                id="dev-font"
                v-model="form.theme_config.typography"
                class="h-11 w-full rounded-control border border-border bg-surface px-4 text-sm text-text-primary outline-none focus:border-primary"
              >
                <option v-for="font in TYPOGRAPHY_OPTIONS" :key="font" :value="font">{{ font }}</option>
              </select>
            </BaseField>

            <BaseField label="Стиль карточек" html-for="dev-card">
              <select
                id="dev-card"
                v-model="form.theme_config.cardStyle"
                class="h-11 w-full rounded-control border border-border bg-surface px-4 text-sm text-text-primary outline-none focus:border-primary"
              >
                <option v-for="option in CARD_STYLE_OPTIONS" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </BaseField>
          </div>

          <div class="flex items-center gap-4">
            <BaseButton tone="light" size="lg" active type="submit">
              {{ isSaving ? 'Сохранение…' : 'Сохранить' }}
            </BaseButton>
            <span v-if="errorText" class="text-sm text-accent">{{ errorText }}</span>
            <span v-else-if="savedAt" class="text-sm text-[#16a34a]">Сохранено</span>
          </div>
        </form>

        <aside class="flex flex-col gap-4">
          <div class="rounded-card bg-surface p-6 shadow-card" :style="previewStyle">
            <h2 class="m-0 mb-4 text-base font-semibold text-text-primary">Превью</h2>

            <div class="overflow-hidden rounded-card border border-border">
              <div class="flex h-28 items-center gap-3 px-5" :style="{ background: 'var(--preview-primary)' }">
                <img v-if="form.logo" :src="form.logo" alt="" class="h-10 w-10 rounded-full object-cover" />
                <span v-else class="grid h-10 w-10 place-items-center rounded-full bg-white/20 font-bold text-white">
                  {{ (form.name.charAt(0) || 'A').toUpperCase() }}
                </span>
                <span class="font-semibold text-white">{{ form.name || 'Застройщик' }}</span>
              </div>

              <div class="flex flex-col gap-3 p-5">
                <span class="text-sm text-text-secondary">{{ form.phone || '+7 (___) ___-__-__' }}</span>
                <button
                  type="button"
                  class="inline-flex h-10 w-fit items-center rounded-full border-0 px-6 text-sm text-white"
                  :style="{ background: 'var(--preview-primary)' }"
                >
                  Смотреть квартиры
                </button>
                <p class="m-0 text-xs text-text-secondary">Шрифт: {{ form.theme_config.typography }}</p>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </template>
  </section>
</template>
