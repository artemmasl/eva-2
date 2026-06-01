import { defineStore } from 'pinia';
import { ref } from 'vue';

import type { ComplexSummary } from '@/core/entities/complex/types';
import { getComplexDetails } from '@/core/entities/complex/use-cases';

export const useComplexStore = defineStore('complex', () => {
  const current = ref<ComplexSummary | null>(null);
  const isLoading = ref(false);

  const loadComplex = async (id: string) => {
    if (current.value?.id === id) {
      return;
    }

    isLoading.value = true;

    try {
      current.value = await getComplexDetails(id);
    } catch {
      current.value = null;
    } finally {
      isLoading.value = false;
    }
  };

  const clearComplex = () => {
    current.value = null;
  };

  return {
    current,
    isLoading,
    loadComplex,
    clearComplex,
  };
});
