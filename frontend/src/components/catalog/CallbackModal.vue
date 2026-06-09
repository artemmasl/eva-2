<script setup lang="ts">
import { ref, watch } from 'vue';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import BaseIconButton from '@/components/common/BaseIconButton.vue';
import BaseInput from '@/components/common/BaseInput.vue';
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
    <BaseIconButton class="absolute right-[18px] top-[18px]" variant="ghost" aria-label="Закрыть" @click="uiStore.closeCallback()">
      <BaseIcon name="close" :size="16" />
    </BaseIconButton>

    <template v-if="!isSubmitted">
      <h2 id="callback-title" :class="$style.title">Обратная связь</h2>
      <p :class="$style.text">Оставьте номер — менеджер перезвонит и ответит на вопросы.</p>

      <form class="flex flex-col gap-3" @submit.prevent="submit">
        <BaseInput v-model="name" type="text" size="lg" placeholder="Ваше имя" />
        <BaseInput v-model="phone" type="tel" size="lg" mask="+7 (###) ###-##-##" placeholder="+7 (___) ___-__-__" />
        <BaseButton type="submit" active size="lg" class="w-full">Жду звонка</BaseButton>
      </form>

      <p :class="$style.fine">Нажимая кнопку, вы соглашаетесь на обработку персональных данных.</p>
    </template>

    <template v-else>
      <h2 id="callback-title" :class="$style.title">Заявка отправлена</h2>
      <p :class="$style.text">Спасибо! Мы свяжемся с вами в ближайшее время.</p>
      <BaseButton active size="lg" class="w-full" @click="uiStore.closeCallback()">Закрыть</BaseButton>
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

.fine {
  margin: 0;
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
