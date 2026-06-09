<script setup lang="ts">
import { nextTick, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import { aiApi, type AiChatContext, type AiSpaceCard } from '@/core/api/ai.api';
import { useStorefrontLink } from '@/core/routing/storefront-link';
import { useComplexStore } from '@/stores/modules/complex.store';
import { useUiStore } from '@/stores/modules/ui.store';

interface AssistantMessage {
  id: number;
  role: 'user' | 'assistant';
  text: string;
  spaces?: AiSpaceCard[];
  followups?: string[];
}

const uiStore = useUiStore();
const complexStore = useComplexStore();
const route = useRoute();
const link = useStorefrontLink();

const messages = ref<AssistantMessage[]>([]);
const draft = ref('');
const isThinking = ref(false);
const scrollEl = ref<HTMLElement>();

let messageId = 0;
let historyLoaded = false;

const startSuggestions = ['Новостройка', 'Студия 3-5 млн', 'Семейная ипотека'];

const STYPE_LABELS: Record<string, string> = {
  parking: 'Паркинг',
  storage: 'Кладовая',
  commercial: 'Коммерция',
};

const cardTitle = (card: AiSpaceCard): string => {
  const base = STYPE_LABELS[card.stype] ?? card.rooms;

  return `${base} · ${card.area} м²`;
};

const formatPrice = (amount: number): string => (
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(amount)
);

const scrollToBottom = () => {
  void nextTick(() => {
    if (scrollEl.value) {
      scrollEl.value.scrollTop = scrollEl.value.scrollHeight;
    }
  });
};

const buildContext = (): AiChatContext => {
  const complexId = (route.params.complexId as string | undefined) ?? complexStore.current?.id;
  const spaceId = route.params.id as string | undefined;

  return {
    page: typeof route.name === 'string' ? route.name : undefined,
    complex_id: complexId,
    complex_name: complexStore.current?.name,
    space_id: spaceId,
  };
};

const loadHistory = async () => {
  if (historyLoaded || messages.value.length) {
    return;
  }

  historyLoaded = true;

  try {
    const history = await aiApi.getHistory();

    messages.value = history.map((item) => ({
      id: messageId += 1,
      role: item.role,
      text: item.content,
    }));

    scrollToBottom();
  } catch {
    // ignore — start with an empty chat
  }
};

const send = async (raw: string) => {
  const text = raw.trim();

  if (!text || isThinking.value) {
    return;
  }

  messages.value.push({ id: messageId += 1, role: 'user', text });
  draft.value = '';
  isThinking.value = true;
  scrollToBottom();

  const reply = ref<AssistantMessage>();

  const ensureReply = (): AssistantMessage => {
    if (!reply.value) {
      reply.value = { id: messageId += 1, role: 'assistant', text: '' };
      messages.value.push(reply.value);
    }

    return reply.value;
  };

  try {
    await aiApi.streamChat(text, buildContext(), {
      onDelta: (chunk) => {
        ensureReply().text += chunk;
        scrollToBottom();
      },
      onCards: (cards) => {
        ensureReply().spaces = cards;
        scrollToBottom();
      },
      onError: (message) => {
        ensureReply().text = message;
      },
    });
  } catch {
    ensureReply().text = 'Не удалось получить ответ. Попробуйте позже.';
  } finally {
    isThinking.value = false;
    scrollToBottom();
  }
};

const resetChat = async () => {
  messages.value = [];
  draft.value = '';

  try {
    await aiApi.resetHistory();
  } catch {
    // ignore — local chat is already cleared
  }
};

const openComplex = () => {
  uiStore.closeAi();
};

watch(() => uiStore.isAiOpen, (open) => {
  if (open) {
    void loadHistory();
    scrollToBottom();
  }
});
</script>

<template>
  <Transition :enter-from-class="$style.enterFrom" :leave-to-class="$style.leaveTo">
    <div v-if="uiStore.isAiOpen" class="fixed inset-0 z-[130]" :class="$style.root">
      <div class="absolute inset-0" :class="$style.overlay" @click="uiStore.closeAi()" />

      <aside :class="$style.panel" role="dialog" aria-modal="true" aria-label="AI-помощник">
        <header :class="$style.header">
          <button type="button" :class="$style.newChat" aria-label="Новый чат" @click="resetChat">＋</button>
          <div :class="$style.brand">
            <span :class="$style.avatar" aria-hidden="true">✦</span>
            <span :class="$style.brandTitle">AI-помощник</span>
          </div>
          <button type="button" :class="$style.close" aria-label="Закрыть" @click="uiStore.closeAi()">✕</button>
        </header>

        <div ref="scrollEl" :class="$style.body">
          <section v-if="!messages.length" :class="$style.start">
            <h2 :class="$style.greeting">Привет, я — AI-помощник</h2>
            <p :class="$style.startText">
              Помогу с подбором квартиры — расскажите, что ищете. Например:
            </p>
            <div :class="$style.chips">
              <button
                v-for="suggestion in startSuggestions"
                :key="suggestion"
                type="button"
                :class="$style.chip"
                @click="send(suggestion)"
              >
                {{ suggestion }}
              </button>
            </div>
          </section>

          <template v-else>
            <div v-for="message in messages" :key="message.id" :class="$style.messageRow">
              <p v-if="message.role === 'user'" :class="$style.userBubble">{{ message.text }}</p>

              <div v-else :class="$style.assistantBlock">
                <p :class="$style.assistantText">{{ message.text }}</p>

                <div v-if="message.spaces?.length" :class="$style.cards">
                  <RouterLink
                    v-for="space in message.spaces"
                    :key="space.id"
                    :class="$style.card"
                    :to="link({ name: 'space-details', params: { complexId: space.complex_id, id: space.id } })"
                    @click="openComplex"
                  >
                    <span :class="$style.cardName">{{ cardTitle(space) }}</span>
                    <span v-if="space.complex_name" :class="$style.cardBadge">{{ space.complex_name }}</span>
                    <span v-if="space.floor" :class="$style.cardBadge">{{ space.floor }} этаж</span>
                    <span :class="$style.cardPrice">{{ formatPrice(space.price) }}</span>
                  </RouterLink>
                </div>

                <div v-if="message.followups?.length" :class="$style.chips">
                  <button
                    v-for="followup in message.followups"
                    :key="followup"
                    type="button"
                    :class="$style.chip"
                    @click="send(followup)"
                  >
                    {{ followup }}
                  </button>
                </div>
              </div>
            </div>

            <p v-if="isThinking" :class="$style.thinking">AI-помощник печатает…</p>
          </template>
        </div>

        <form :class="$style.composer" @submit.prevent="send(draft)">
          <input v-model="draft" type="text" :class="$style.input" placeholder="Спросите AI-помощника" />
          <button type="submit" :class="$style.sendButton" aria-label="Отправить" :disabled="isThinking">✦</button>
        </form>
      </aside>
    </div>
  </Transition>
</template>

<style module lang="scss">
.root {
  transition: opacity 0.25s ease;

  &.enterFrom,
  &.leaveTo {
    opacity: 0;

    .panel {
      transform: translateX(-100%);
    }
  }
}

.overlay {
  background: rgba(17, 17, 17, 0.4);
}

.panel {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  width: 460px;
  max-width: 92vw;
  height: 100%;
  background: var(--color-surface);
  border-top-right-radius: 32px;
  border-bottom-right-radius: 32px;
  box-shadow: var(--shadow-floating);
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.header {
  display: grid;
  grid-template-columns: 40px 1fr 40px;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.brand {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
}

.avatar {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  font-size: 14px;
  color: var(--color-text-inverse);
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  border-radius: var(--radius-pill);
}

.brandTitle {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.newChat,
.close {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  font-size: 16px;
  color: var(--color-text-secondary);
  cursor: pointer;
  background: var(--color-surface-control);
  border: 0;
  border-radius: var(--radius-pill);
}

.body {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 18px;
  padding: 24px;
  overflow-y: auto;
}

.start {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: auto 0;
  text-align: center;
}

.greeting {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.startText {
  margin: 0;
  color: var(--color-text-secondary);
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.chip {
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-inverse);
  cursor: pointer;
  background: var(--color-primary);
  border: 0;
  border-radius: var(--radius-pill);
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.9;
  }
}

.messageRow {
  display: flex;
  flex-direction: column;
}

.userBubble {
  align-self: flex-end;
  max-width: 80%;
  margin: 0;
  padding: 10px 16px;
  color: var(--color-text-inverse);
  background: var(--color-primary);
  border-radius: 18px 18px 4px 18px;
}

.assistantBlock {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.assistantText {
  margin: 0;
  color: var(--color-text-primary);
}

.cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  width: 100%;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px;
  text-decoration: none;
  background: var(--color-surface-muted);
  border: 1px solid transparent;
  border-radius: 16px;
  transition: border-color 140ms ease;

  &:hover {
    border-color: var(--color-primary);
  }
}

.cardCover {
  display: grid;
  place-items: center;
  height: 64px;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-inverse);
  background: linear-gradient(135deg, #1f2a44, #6b7fb0);
  border-radius: 12px;
}

.cardName {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.cardBadge {
  font-size: 11px;
  color: var(--color-text-secondary);
}

.cardPrice {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.thinking {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.composer {
  display: flex;
  gap: 10px;
  padding: 18px 24px;
  border-top: 1px solid var(--color-border);
}

.input {
  flex: 1;
  height: 48px;
  padding: 0 18px;
  font-size: 15px;
  color: var(--color-text-primary);
  background: var(--color-surface-control);
  border: 1px solid transparent;
  border-radius: var(--radius-pill);
  outline: none;

  &:focus {
    border-color: var(--color-primary);
  }
}

.sendButton {
  display: grid;
  flex-shrink: 0;
  place-items: center;
  width: 48px;
  height: 48px;
  color: var(--color-text-inverse);
  cursor: pointer;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  border: 0;
  border-radius: var(--radius-pill);

  &:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
}
</style>
