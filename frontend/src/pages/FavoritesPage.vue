<script setup lang="ts">
import { computed, ref } from 'vue';

import SpaceCard from '@/components/catalog/SpaceCard.vue';
import BaseButton from '@/components/common/BaseButton.vue';
import BaseChip from '@/components/common/BaseChip.vue';
import BaseDropdown from '@/components/common/BaseDropdown.vue';
import BaseIcon from '@/components/common/BaseIcon.vue';
import BaseInput from '@/components/common/BaseInput.vue';
import {
  GENERAL_COLLECTION_ID,
  useFavoritesStore,
  type FavoriteStype,
} from '@/stores/modules/favorites.store';

const favoritesStore = useFavoritesStore();

const stypeOptions: { label: string; value: FavoriteStype }[] = [
  { label: 'Все объекты', value: 'all' },
  { label: 'Квартиры', value: 'flat' },
  { label: 'Парковки', value: 'parking' },
  { label: 'Кладовки', value: 'storage' },
  { label: 'Коммерция', value: 'commercial' },
];

const isCreating = ref(false);
const newCollectionName = ref('');
const shareMessage = ref('');

const activeCollectionName = computed(() => {
  if (favoritesStore.activeCollectionId === GENERAL_COLLECTION_ID) {
    return 'Общий список';
  }

  return favoritesStore.collections.find(
    (collection) => collection.id === favoritesStore.activeCollectionId,
  )?.name ?? 'Общий список';
});

const isGeneralActive = computed(() => favoritesStore.activeCollectionId === GENERAL_COLLECTION_ID);

const startCreating = () => {
  isCreating.value = true;
  newCollectionName.value = '';
};

const confirmCreate = () => {
  const id = favoritesStore.createCollection(newCollectionName.value);

  if (id) {
    favoritesStore.setActiveCollection(id);
  }

  isCreating.value = false;
  newCollectionName.value = '';
};

const removeActiveCollection = () => {
  if (!isGeneralActive.value) {
    favoritesStore.removeCollection(favoritesStore.activeCollectionId);
  }
};

const shareCollection = async () => {
  const ids = favoritesStore.visibleItems.map((item) => item.spaceId).join(',');
  const url = `${window.location.origin}/favorites?ids=${encodeURIComponent(ids)}`;

  try {
    await navigator.clipboard.writeText(url);
    shareMessage.value = 'Ссылка скопирована';
  } catch {
    shareMessage.value = url;
  }

  window.setTimeout(() => {
    shareMessage.value = '';
  }, 2400);
};
</script>

<template>
  <main class="mx-auto flex w-full grow flex-col gap-6" :class="$style.page">
    <header class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex flex-wrap items-center gap-5">
        <h1 class="m-0 text-2xl font-medium">Мое избранное</h1>
        <div class="flex flex-wrap gap-2">
          <BaseChip
            v-for="option in stypeOptions"
            :key="option.value"
            :active="favoritesStore.activeStype === option.value"
            @click="favoritesStore.setActiveStype(option.value)"
          >
            {{ option.label }}
          </BaseChip>
        </div>
      </div>

      <div class="flex items-center gap-4 text-sm">
        <span v-if="shareMessage" class="text-primary">{{ shareMessage }}</span>
        <button
          type="button"
          class="inline-flex cursor-pointer items-center gap-2 border-0 bg-transparent text-primary"
          @click="shareCollection"
        >
          <BaseIcon name="share" :size="17" />
          Поделиться подборкой
        </button>
        <button
          type="button"
          class="inline-flex cursor-pointer items-center gap-2 border-0 bg-transparent text-text-secondary disabled:opacity-40"
          :disabled="isGeneralActive"
          @click="removeActiveCollection"
        >
          <BaseIcon name="trash" :size="17" />
          Удалить подборку
        </button>
      </div>
    </header>

    <div class="grid items-start gap-6" :class="$style.layout">
      <aside class="flex flex-col gap-1 rounded-3xl p-3" :class="$style.sidebar">
        <button
          type="button"
          class="flex h-12 cursor-pointer items-center justify-between rounded-2xl border-0 px-4 text-sm transition-colors"
          :class="isGeneralActive ? 'bg-[#2945ff] text-white' : 'bg-transparent text-[#111827] hover:bg-white/60'"
          @click="favoritesStore.setActiveCollection(GENERAL_COLLECTION_ID)"
        >
          <span>Общий список</span>
          <span :class="isGeneralActive ? 'text-white/80' : 'text-[#94a3b8]'">{{ favoritesStore.generalCount }}</span>
        </button>

        <button
          v-for="collection in favoritesStore.collections"
          :key="collection.id"
          type="button"
          class="flex h-12 cursor-pointer items-center justify-between rounded-2xl border-0 px-4 text-sm transition-colors"
          :class="favoritesStore.activeCollectionId === collection.id
            ? 'bg-[#2945ff] text-white'
            : 'bg-transparent text-[#111827] hover:bg-white/60'"
          @click="favoritesStore.setActiveCollection(collection.id)"
        >
          <span class="truncate">{{ collection.name }}</span>
          <span :class="favoritesStore.activeCollectionId === collection.id ? 'text-white/80' : 'text-[#94a3b8]'">
            {{ favoritesStore.countForCollection(collection.id) }}
          </span>
        </button>

        <button
          v-if="!isCreating"
          type="button"
          class="mt-1 flex h-12 cursor-pointer items-center gap-2 rounded-2xl border-0 bg-transparent px-4 text-sm text-primary"
          @click="startCreating"
        >
          <BaseIcon name="plus-circle" :size="18" />
          Новая подборка
        </button>

        <div v-else class="mt-1 flex items-center gap-2 px-1">
          <BaseInput
            v-model="newCollectionName"
            type="text"
            placeholder="Название подборки"
            @keyup.enter="confirmCreate"
            @keyup.esc="isCreating = false"
          />
          <BaseButton active class="h-10 w-10 shrink-0 px-0" @click="confirmCreate">OK</BaseButton>
        </div>
      </aside>

      <section>
        <TransitionGroup
          name="favorite-card"
          tag="div"
          class="grid grid-cols-3 gap-6 max-[1180px]:grid-cols-2 max-[720px]:grid-cols-1"
        >
          <div v-for="item in favoritesStore.visibleItems" :key="item.spaceId" class="relative min-w-0">
            <SpaceCard :space="item.space" />
            <div v-if="favoritesStore.collections.length" class="absolute left-3.5 top-3.5 z-10">
              <BaseDropdown
                :model-value="''"
                :options="favoritesStore.collections.map((collection) => ({
                  label: item.collectionIds.includes(collection.id) ? `✓ ${collection.name}` : collection.name,
                  value: collection.id,
                }))"
                placeholder="Подборки"
                @change="(id) => id && favoritesStore.toggleCollectionMembership(item.spaceId, id)"
              />
            </div>
          </div>
          <p
            v-if="favoritesStore.visibleItems.length === 0"
            key="empty"
            class="col-span-full rounded-3xl bg-white p-12 text-center text-[#6b7280]"
          >
            В подборке «{{ activeCollectionName }}» пока нет объектов
          </p>
        </TransitionGroup>
      </section>
    </div>
  </main>
</template>

<style module lang="scss">
.page {
  max-width: 1328px;
}

.layout {
  grid-template-columns: 280px 1fr;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

.sidebar {
  background: var(--color-surface-control, #eef1f8);

  @media (max-width: 900px) {
    flex-direction: row;
    overflow-x: auto;
  }
}
</style>

<style scoped>
.favorite-card-move {
  transition: transform 260ms cubic-bezier(0.16, 1, 0.3, 1);
}

.favorite-card-leave-active {
  position: absolute;
  transition: opacity 180ms ease-out, transform 180ms ease-out;
}

.favorite-card-leave-to {
  opacity: 0;
  transform: scale(0.96);
}

.favorite-card-enter-active {
  transition: opacity 260ms ease-out, transform 260ms cubic-bezier(0.16, 1, 0.3, 1);
}

.favorite-card-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
</style>
