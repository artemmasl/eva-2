import { defineStore } from 'pinia';
import { ref } from 'vue';

import { getSpaceDetails } from '@/core/entities/space/use-cases';
import type { Space } from '@/core/entities/space/types';

export const useSpaceDetailsStore = defineStore('spaceDetails', () => {
  const space = ref<Space | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const loadSpace = async (id: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      space.value = await getSpaceDetails(id);
    } catch {
      space.value = null;
      error.value = 'Не удалось загрузить помещение';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    space,
    isLoading,
    error,
    loadSpace,
  };
});
