<template>
  <main class="mx-auto flex w-full grow flex-col" :class="$style.contentWidth">
    <div :class="[$style.contentFrame, 'relative min-h-60', catalogStore.isLoading && catalogStore.spaces.length > 0 && $style.contentLoading]">
      <SpacesVisualView v-if="activeView === 'visual'" />
      <SpacesChessView v-else-if="activeView === 'chess'" />
      <template v-else>
        <SpaceList :spaces="catalogStore.visibleSpaces" />
        <div ref="loadMoreTrigger" class="min-h-12">
          <p v-if="catalogStore.isLoadingMore" class="rounded-3xl bg-white p-10">Loading...</p>
        </div>
      </template>
      <Transition name="loading-overlay">
        <div
          v-if="catalogStore.isLoading"
          v-motion
          :class="[
            'pointer-events-none absolute inset-0 grid items-start justify-items-center rounded-3xl',
            $style.loadingOverlay,
            catalogStore.spaces.length === 0 && ['items-center pt-0', $style.loadingOverlayEmpty],
          ]"
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1, transition: { duration: 160, ease: 'easeOut' } }"
        >
          <span class="animate-pulse rounded-full px-5 py-3" :class="$style.loadingPill">Loading...</span>
        </div>
      </Transition>
    </div>
  </main>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import SpaceList from '@/components/catalog/SpaceList.vue';
import SpacesChessView from '@/components/catalog/SpacesChessView.vue';
import SpacesVisualView from '@/components/catalog/SpacesVisualView.vue';
import { resolveCatalogView } from '@/core/catalog/views';
import { useCatalogStore } from '@/stores/modules/catalog.store';

const route = useRoute();
const catalogStore = useCatalogStore();
const activeView = computed(() => resolveCatalogView(route.query.view));
const loadMoreTrigger = ref<HTMLElement>();
let loadMoreObserver: IntersectionObserver | null = null;

watch(
  () => route.params.complexId,
  (complexId) => {
    catalogStore.setComplexId(complexId ? String(complexId) : null);
    void catalogStore.loadCatalog();
  },
);

onMounted(() => {
  catalogStore.setComplexId(route.params.complexId ? String(route.params.complexId) : null);
  void catalogStore.loadCatalog();

  loadMoreObserver = new IntersectionObserver(
    (entries) => {
      if (entries[0]?.isIntersecting) {
        void catalogStore.loadMoreSpaces();
      }
    },
    { rootMargin: '360px 0px' },
  );

  if (loadMoreTrigger.value) {
    loadMoreObserver.observe(loadMoreTrigger.value);
  }
});

// The infinite-scroll trigger is only rendered in the plans view; re-observe it
// whenever it re-mounts after switching back from visual/chess.
watch(loadMoreTrigger, (element) => {
  if (loadMoreObserver && element) {
    loadMoreObserver.observe(element);
  }
});

onBeforeUnmount(() => {
  loadMoreObserver?.disconnect();
});
</script>

<style module lang="scss">
.contentWidth {
  max-width: 1328px;
}

.contentFrame {
  z-index: 0;

  section {
    transition:
      opacity 200ms ease-in-out;
  }
}

.contentLoading {
  section {
    opacity: 0.58;
  }
}

.loadingOverlay {
  z-index: 3;
  padding-top: 76px;
}

.loadingOverlayEmpty {
  background: rgba(246, 244, 239, 0.78);
}

.loadingPill {
  color: var(--color-text-primary);
  background: color-mix(in srgb, var(--color-surface) 90%, transparent);
  box-shadow: var(--shadow-card);
}
</style>

<style scoped>
.loading-overlay-leave-active {
  transition: opacity 160ms ease-out;
}

.loading-overlay-leave-to {
  opacity: 0;
}
</style>
