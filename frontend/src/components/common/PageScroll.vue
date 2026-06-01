<template>
  <div class="relative min-h-0">
    <div
      ref="container"
      class="h-full overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
      @scroll="updateScrollbar"
      @mouseenter="visible = true"
      @mouseleave="hideScrollbar"
    >
      <slot />
    </div>

    <div
      ref="scrollbar"
      class="pointer-events-none absolute bottom-3 right-1 top-3 w-2 origin-center transition-[opacity,transform] duration-200 ease-out"
      :style="scrollbarStyle"
    >
      <div class="relative h-full">
        <div
          ref="slider"
          class="absolute w-full rounded-full bg-[#2945ff] transition-[height,transform] duration-200 ease-out"
          :style="sliderStyle"
        />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const container = ref<HTMLDivElement>()

const visible = ref(false)

const sliderHeight = ref(0)
const sliderTop = ref(0)

let timeout: number

const scrollbarStyle = computed(() => ({
  opacity: visible.value ? 1 : 0,
  transform: `scaleX(${visible.value ? 1 : 0.7})`,
}))

const sliderStyle = computed(() => ({
  height: `${sliderHeight.value}px`,
  transform: `translateY(${sliderTop.value}px)`,
  transformOrigin: '50% 0%',
}))

const updateScrollbar = () => {
  const el = container.value

  if (!el) {
    return
  }

  const ratio = el.clientHeight / el.scrollHeight
  const hasOverflow = ratio < 1

  if (!hasOverflow) {
    visible.value = false
    return
  }

  sliderHeight.value = Math.max(el.clientHeight * ratio, 40)

  sliderTop.value =
    (el.scrollTop / (el.scrollHeight - el.clientHeight))
    * (el.clientHeight - sliderHeight.value)

  visible.value = true

  clearTimeout(timeout)

  timeout = window.setTimeout(() => {
    visible.value = false
  }, 1000)
}

const hideScrollbar = () => {
  clearTimeout(timeout)

  timeout = window.setTimeout(() => {
    visible.value = false
  }, 300)
}

onMounted(() => {
  updateScrollbar()
})

onBeforeUnmount(() => {
  clearTimeout(timeout)
})
</script>

