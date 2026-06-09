<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseField from '@/components/common/BaseField.vue';
import BaseInput from '@/components/common/BaseInput.vue';
import { useAdminStore } from '@/stores/modules/admin.store';

const adminStore = useAdminStore();
const router = useRouter();
const route = useRoute();

const password = ref('');
const error = ref<string | null>(null);
const isLoading = ref(false);

const submit = async () => {
  error.value = null;
  isLoading.value = true;

  try {
    await adminStore.login(password.value);

    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : null;
    await router.push(redirect ?? { name: 'admin-developers' });
  } catch {
    error.value = 'Неверный пароль';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="grid min-h-screen place-items-center bg-surface-control px-6">
    <form class="w-full max-w-[380px] rounded-card bg-surface p-8 shadow-card" @submit.prevent="submit">
      <div class="mb-6 flex flex-col items-center gap-3 text-center">
        <span class="grid h-12 w-12 place-items-center rounded-control bg-primary text-text-inverse text-xl font-bold">A</span>
        <h1 class="m-0 text-xl font-semibold text-text-primary">Админка застройщиков</h1>
        <p class="m-0 text-sm text-text-secondary">Войдите, чтобы редактировать застройщиков</p>
      </div>

      <BaseField label="Пароль" :error="error ?? undefined" html-for="admin-password">
        <BaseInput
          id="admin-password"
          v-model="password"
          type="password"
          tone="surface"
          placeholder="Введите пароль"
          :invalid="Boolean(error)"
        />
      </BaseField>

      <BaseButton class="mt-6 w-full" tone="light" size="lg" active type="submit">
        {{ isLoading ? 'Вход…' : 'Войти' }}
      </BaseButton>
    </form>
  </div>
</template>
