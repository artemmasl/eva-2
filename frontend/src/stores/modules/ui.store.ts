import { defineStore } from 'pinia';
import { ref } from 'vue';

import type { LeadKind } from '@/core/entities/lead/types';
import type { Space } from '@/core/entities/space/types';

export interface CallbackContext {
  kind: LeadKind;
  title: string;
  description: string;
  spaceId?: string | null;
  complexId?: string | null;
}

const DEFAULT_CALLBACK_CONTEXT: CallbackContext = {
  kind: 'callback',
  title: 'Обратная связь',
  description: 'Оставьте номер — менеджер перезвонит и ответит на вопросы.',
  spaceId: null,
  complexId: null,
};

export const useUiStore = defineStore('ui', () => {
  const isSideMenuOpen = ref(false);
  const isAiOpen = ref(false);
  const isCallbackOpen = ref(false);
  const callbackContext = ref<CallbackContext>({ ...DEFAULT_CALLBACK_CONTEXT });
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

  const openAi = () => {
    isAiOpen.value = true;
  };

  const closeAi = () => {
    isAiOpen.value = false;
  };

  const openCallback = (context?: Partial<CallbackContext>) => {
    callbackContext.value = { ...DEFAULT_CALLBACK_CONTEXT, ...context };
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
    isAiOpen,
    openAi,
    closeAi,
    isCallbackOpen,
    callbackContext,
    openCallback,
    closeCallback,
    isSameLayoutOpen,
    sameLayoutSpace,
    openSameLayout,
    closeSameLayout,
  };
});
