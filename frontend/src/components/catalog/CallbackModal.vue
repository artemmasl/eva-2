<script setup lang="ts">
import { ref, watch } from 'vue';

import BaseModal from '@/components/common/BaseModal.vue';
import { useUiStore } from '@/stores/modules/ui.store';

const uiStore = useUiStore();

const name = ref('');
const phone = ref('');
const isSubmitted = ref(false);

const reset = () => {
  name.value = '';
  phone.value = '';
  isSubmitted.value = false;
};

watch(() => uiStore.isCallbackOpen, (open) => {
  if (open) {
    reset();
  }
});

const submit = () => {
  if (!phone.value.trim()) {
    return;
  }

  // No backend yet — acknowledge the request locally.
  isSubmitted.value = true;
};
</script>

<template>
  <BaseModal
    v-if="uiStore.isCallbackOpen"
    labelled-by="callback-title"
    :panel-class="$style.panel"
    @close="uiStore.closeCallback()"
  >
    <button type="button" :class="$style.close" aria-label="Закрыть" @click="uiStore.closeCallback()">✕</button>

    <template v-if="!isSubmitted">
      <h2 id="callback-title" :class="$style.title">Обратная связь</h2>
      <p :class="$style.text">Оставьте номер — менеджер перезвонит и ответит на вопросы.</p>

      <form class="flex flex-col gap-3" @submit.prevent="submit">
        <input v-model="name" type="text" :class="$style.input" placeholder="Ваше имя" />
        <input v-model="phone" type="tel" :class="$style.input" placeholder="Телефон" required />
        <button type="submit" :class="$style.cta">Жду звонка</button>
      </form>

      <p :class="$style.fine">Нажимая кнопку, вы соглашаетесь на обработку персональных данных.</p>
    </template>

    <template v-else>
      <h2 id="callback-title" :class="$style.title">Заявка отправлена</h2>
      <p :class="$style.text">Спасибо! Мы свяжемся с вами в ближайшее время.</p>
      <button type="button" :class="$style.cta" @click="uiStore.closeCallback()">Закрыть</button>
    </template>
  </BaseModal>
</template>

<style module lang="scss">
.panel {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
  max-width: 420px;
  padding: 32px;
  background: var(--color-surface);
  border-radius: 28px;
  box-shadow: var(--shadow-modal);

  @media (max-width: 900px) {
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }
}

.close {
  position: absolute;
  top: 18px;
  right: 18px;
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  color: var(--color-text-secondary);
  cursor: pointer;
  background: var(--color-surface-control);
  border: 0;
  border-radius: var(--radius-pill);
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.text {
  margin: 0;
  color: var(--color-text-secondary);
}

.input {
  height: 48px;
  padding: 0 18px;
  font-size: 15px;
  color: var(--color-text-primary);
  background: var(--color-surface-control);
  border: 1px solid transparent;
  border-radius: var(--radius-control);
  outline: none;

  &:focus {
    border-color: var(--color-primary);
  }
}

.cta {
  height: 48px;
  font-weight: 600;
  color: var(--color-text-inverse);
  cursor: pointer;
  background: var(--color-primary);
  border: 0;
  border-radius: var(--radius-pill);
}

.fine {
  margin: 0;
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
