<script setup lang="ts">
import { computed } from 'vue';

import type { PlanAsset, PlanRegion } from '@/core/entities/plan/types';

const props = withDefaults(defineProps<{
  asset: PlanAsset | null;
  regions: PlanRegion[];
  selectedId?: string | null;
  dimmedIds?: string[];
}>(), {
  selectedId: null,
  dimmedIds: () => [],
});

const emit = defineEmits<{
  select: [region: PlanRegion];
}>();

const aspectRatio = computed(() => {
  if (props.asset && props.asset.width > 0 && props.asset.height > 0) {
    return `${props.asset.width} / ${props.asset.height}`;
  }

  return '16 / 9';
});

const toPoints = (region: PlanRegion): string => (
  region.points.map(([x, y]) => `${x * 100},${y * 100}`).join(' ')
);

const centroid = (region: PlanRegion): { x: number; y: number } => {
  const total = region.points.reduce(
    (acc, [x, y]) => ({ x: acc.x + x, y: acc.y + y }),
    { x: 0, y: 0 },
  );
  const count = region.points.length || 1;

  return { x: (total.x / count) * 100, y: (total.y / count) * 100 };
};

const isDimmed = (region: PlanRegion): boolean => (
  props.dimmedIds.includes(region.id) || region.status !== 'available'
);
</script>

<template>
  <div :class="$style.viewer" :style="{ aspectRatio }">
    <img v-if="asset && asset.image_url" :class="$style.image" :src="asset.image_url" alt="" />

    <svg :class="$style.overlay" viewBox="0 0 100 100" preserveAspectRatio="none">
      <g
        v-for="region in regions"
        :key="region.id"
        :class="[
          $style.region,
          isDimmed(region) && $style.regionDimmed,
          selectedId === region.id && $style.regionSelected,
        ]"
        @click="emit('select', region)"
      >
        <polygon :points="toPoints(region)" />
        <text
          v-if="region.label"
          :x="centroid(region).x"
          :y="centroid(region).y"
          text-anchor="middle"
          dominant-baseline="middle"
        >
          {{ region.label }}
        </text>
      </g>
    </svg>
  </div>
</template>

<style module lang="scss">
.viewer {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: 24px;
  background: linear-gradient(135deg, #1f2a44 0%, #3a4d7a 55%, #6b7fb0 100%);
  box-shadow: var(--shadow-card);
}

.image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.region {
  cursor: pointer;

  polygon {
    fill: color-mix(in srgb, var(--color-primary) 32%, transparent);
    stroke: #fff;
    stroke-width: 0.4;
    transition: fill 140ms ease;
    vector-effect: non-scaling-stroke;
  }

  text {
    fill: #fff;
    font-size: 3px;
    font-weight: 600;
    paint-order: stroke;
    stroke: rgba(0, 0, 0, 0.35);
    stroke-width: 0.6;
    pointer-events: none;
  }

  &:hover polygon {
    fill: color-mix(in srgb, var(--color-primary) 62%, transparent);
  }
}

.regionDimmed {
  cursor: not-allowed;

  polygon {
    fill: rgba(15, 23, 42, 0.45);
    stroke: rgba(255, 255, 255, 0.5);
  }

  &:hover polygon {
    fill: rgba(15, 23, 42, 0.5);
  }
}

.regionSelected polygon {
  fill: color-mix(in srgb, var(--color-primary) 72%, transparent);
}
</style>
