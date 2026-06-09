import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

import { adminApi } from '@/core/api/admin.api';

const STORAGE_KEY = 'eva_admin_token';

export const useAdminStore = defineStore('admin', () => {
  const token = ref<string | null>(localStorage.getItem(STORAGE_KEY));
  const isAuthenticated = computed(() => Boolean(token.value));

  const login = async (password: string) => {
    const { token: issued } = await adminApi.login(password);

    token.value = issued;
    localStorage.setItem(STORAGE_KEY, issued);
  };

  const logout = () => {
    token.value = null;
    localStorage.removeItem(STORAGE_KEY);
  };

  return {
    token,
    isAuthenticated,
    login,
    logout,
  };
});
