<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue';

import SpaceCard from '@/components/catalog/SpaceCard.vue';
import type { Space } from '@/core/entities/space/types';

const props = defineProps<{
  spaces: Space[];
}>();

const animatedSpaceIds = ref(new Set<string>());
const seenSpaceIds = ref(new Set<string>());
let previousSpaceIds: string[] = [];
let animationTimeout: ReturnType<typeof setTimeout> | undefined;

const enterAnimationDuration = 520;
const enterAnimationMaxDelay = 160;

const isAppendUpdate = (previousIds: string[], nextIds: string[]): boolean => (
  previousIds.length > 0 &&
  nextIds.length >= previousIds.length &&
  previousIds.every((id, index) => nextIds[index] === id)
);

const queueCardAnimations = (spaces: Space[]) => {
  const nextIds = spaces.map((space) => space.id);
  const isFreshList = !isAppendUpdate(previousSpaceIds, nextIds);
  const nextSeenIds = isFreshList ? new Set<string>() : new Set(seenSpaceIds.value);
  const nextAnimatedIds = new Set<string>();

  nextIds.forEach((id) => {
    if (!nextSeenIds.has(id)) {
      nextAnimatedIds.add(id);
    }

    nextSeenIds.add(id);
  });

  seenSpaceIds.value = nextSeenIds;
  animatedSpaceIds.value = nextAnimatedIds;
  previousSpaceIds = nextIds;

  if (animationTimeout) {
    clearTimeout(animationTimeout);
  }

  if (nextAnimatedIds.size > 0) {
    animationTimeout = setTimeout(() => {
      animatedSpaceIds.value = new Set();
      animationTimeout = undefined;
    }, enterAnimationDuration + enterAnimationMaxDelay);
  }
};

const isSpaceAnimating = (spaceId: string): boolean => animatedSpaceIds.value.has(spaceId);

const getAnimationDelay = (spaceId: string): string => {
  const animationIndex = Array.from(animatedSpaceIds.value).indexOf(spaceId);

  return `${Math.min(Math.max(animationIndex, 0) * 24, enterAnimationMaxDelay)}ms`;
};

watch(() => props.spaces, queueCardAnimations, { immediate: true });

onBeforeUnmount(() => {
  if (animationTimeout) {
    clearTimeout(animationTimeout);
  }
});
</script>

<template>
  <TransitionGroup
    name="space-card"
    tag="section"
    class="grid grid-cols-4 gap-6 max-[1180px]:grid-cols-3 max-[860px]:grid-cols-2 max-[560px]:grid-cols-1"
  >
    <div
      v-for="space in props.spaces"
      :key="space.id"
      class="min-w-0"
      :class="{ [$style.enteringCard]: isSpaceAnimating(space.id) }"
      :style="{ '--space-card-delay': getAnimationDelay(space.id) }"
    >
      <SpaceCard :space="space" />
    </div>
    <p v-if="props.spaces.length === 0" key="empty" class="col-span-full rounded-3xl bg-white p-12 text-center text-[#6b7280]">Квартиры не найдены</p>
  </TransitionGroup>
</template>

<style module lang="scss">
.enteringCard {
  opacity: 0;
  animation: space-card-enter 520ms cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-delay: var(--space-card-delay, 0ms);
  backface-visibility: hidden;
  transform: translate3d(0, 0, 0);

  @media (prefers-reduced-motion: reduce) {
    opacity: 1;
    animation: none;
  }
}

@keyframes space-card-enter {
  from {
    opacity: 0;
    transform: translate3d(0, 14px, 0) scale(0.985);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0) scale(1);
  }
}
</style>

<style scoped>
.space-card-move {
  transition: transform 260ms cubic-bezier(0.16, 1, 0.3, 1);
}

.space-card-leave-active {
  transition: opacity 140ms ease-out;
}

.space-card-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  :global(.space-card-move),
  :global(.space-card-leave-active) {
    transition: none;
  }
}
</style>
