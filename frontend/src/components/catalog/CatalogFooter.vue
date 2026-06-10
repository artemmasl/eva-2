<script setup lang="ts">
import { computed } from 'vue';

import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useTenantStore } from '@/stores/modules/tenant.store';

const link = useStorefrontLink();
const tenantStore = useTenantStore();

const homeTo = computed(() => link({ name: 'complexes' }));
const privacyTo = computed(() => link({ name: 'privacy' }));

const developer = computed(() => tenantStore.tenant?.developer ?? null);
const developerName = computed(() => developer.value?.name ?? '');
const phone = computed(() => developer.value?.phone ?? '');
const phoneHref = computed(() => `tel:${phone.value.replace(/[^\d+]/g, '')}`);
const email = computed(() => developer.value?.email ?? '');
const website = computed(() => developer.value?.website ?? '');
const websiteLabel = computed(() => website.value.replace(/^https?:\/\//, '').replace(/\/$/, ''));
const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="mx-auto mt-12 max-w-[1240px]">
    <div class="grid grid-cols-[auto_1.3fr_1fr] items-center gap-10 rounded-[28px] bg-white px-9 py-7 max-[900px]:grid-cols-1 max-[900px]:gap-6">
      <RouterLink class="grid h-[42px] w-[42px] place-items-center text-[34px] font-black text-[#0b2447] no-underline" :to="homeTo">A</RouterLink>

      <div class="flex flex-wrap gap-x-[18px] gap-y-2 text-xs text-[#111827] [&_a]:text-[#2348ff] [&_a]:no-underline [&_span]:w-full">
        <span>Отдел продаж:</span>
        <a v-if="phone" :href="phoneHref">{{ phone }}</a>
        <a v-if="email" :href="`mailto:${email}`">{{ email }}</a>
        <a v-if="website" :href="website" target="_blank" rel="noopener">{{ websiteLabel }}</a>
      </div>

      <nav class="flex flex-wrap gap-x-[18px] gap-y-2 text-xs text-[#111827] [&_a]:text-[#2348ff] [&_a]:no-underline [&_span]:w-full" aria-label="Footer tenants navigation">
        <span>Для агентов</span>
        <a href="#">Зафиксировать клиента</a>
        <a href="#">Регистрация агента</a>
      </nav>
    </div>

    <div class="flex flex-wrap justify-between gap-4 px-7 pt-6 text-[11px] text-[#6b7280] [&_a]:text-[#2348ff] [&_a]:no-underline">
      <span>©{{ currentYear }}<template v-if="developerName"> {{ developerName }}</template></span>
      <RouterLink :to="privacyTo">Политика конфиденциальности</RouterLink>
      <span>Разработано на платформе</span>
    </div>
  </footer>
</template>
