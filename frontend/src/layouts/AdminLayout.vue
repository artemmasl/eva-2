<script setup lang="ts">
import { useRouter } from 'vue-router';

import BaseButton from '@/components/common/BaseButton.vue';
import { useAdminStore } from '@/stores/modules/admin.store';

const adminStore = useAdminStore();
const router = useRouter();

const logout = () => {
  adminStore.logout();
  void router.push({ name: 'admin-login' });
};
</script>

<template>
  <div class="min-h-screen bg-surface-control text-text-primary">
    <header class="border-b border-border bg-surface">
      <div class="mx-auto flex h-16 w-full max-w-[1100px] items-center justify-between px-6">
        <RouterLink :to="{ name: 'admin-developers' }" class="flex items-center gap-2 no-underline">
          <span class="grid h-9 w-9 place-items-center rounded-control bg-primary text-text-inverse font-bold">A</span>
          <span class="text-base font-semibold text-text-primary">EVA Admin</span>
        </RouterLink>

        <BaseButton tone="outline" size="md" @click="logout">Выйти</BaseButton>
      </div>
    </header>

    <main class="mx-auto w-full max-w-[1100px] px-6 py-10">
      <RouterView />
    </main>
  </div>
</template>
