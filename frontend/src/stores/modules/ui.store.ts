import { defineStore } from 'pinia';
import { ref } from 'vue';

import type { Space } from '@/core/entities/space/types';

export const useUiStore = defineStore('ui', () => {
  const isSideMenuOpen = ref(false);
  const isCallbackOpen = ref(false);
  const isSameLayoutOpen = ref(false);
  const sameLayoutSpace = ref<Space | null>(null);

  const openSideMenu = () => {
    isSideMenuOpen.value = true;
  };

  const closeSideMenu = () => {
    isSideMenuOpen.value = false;
  };

  const toggleSideMenu = () => {
    isSideMenuOpen.value = !isSideMenuOpen.value;
  };

  const openCallback = () => {
    isSideMenuOpen.value = false;
    isCallbackOpen.value = true;
  };

  const closeCallback = () => {
    isCallbackOpen.value = false;
  };

  const openSameLayout = (space: Space) => {
    sameLayoutSpace.value = space;
    isSameLayoutOpen.value = true;
  };

  const closeSameLayout = () => {
    isSameLayoutOpen.value = false;
    sameLayoutSpace.value = null;
  };

  return {
    isSideMenuOpen,
    openSideMenu,
    closeSideMenu,
    toggleSideMenu,
    isCallbackOpen,
    openCallback,
    closeCallback,
    isSameLayoutOpen,
    sameLayoutSpace,
    openSameLayout,
    closeSameLayout,
  };
});
