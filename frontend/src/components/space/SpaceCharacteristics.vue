<script setup lang="ts">
import type { Space } from '@/core/entities/space/types';

defineProps<{
  space: Space;
}>();
</script>

<template>
  <dl>
    <dt>Rooms</dt>
    <dd>{{ space.rooms }}</dd>
    <dt>Area</dt>
    <dd>{{ space.area }} m²</dd>
    <dt>Floor</dt>
    <dd>{{ space.floor }}</dd>
    <dt>Status</dt>
    <dd>{{ space.status }}</dd>
  </dl>
</template>
