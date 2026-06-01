# Frontend Style Guide

## Styling strategy

The project uses a hybrid styling model:

- Tailwind CSS is used for layout, spacing, sizing helpers, grids, flexbox, and simple typography utilities.
- SCSS modules are preferred for component-specific visual styling.
- Global styles are limited to reset/base rules, application root styles, font setup, and design tokens.
- CSS custom properties are the source of truth for colors, shadows, radii, and other reusable theme values.

## Tailwind usage

Use Tailwind for simple, standard utilities:

```vue
<div class="grid gap-4 p-4">
```

Preferred utility categories:

- display and layout: `flex`, `grid`, `items-center`, `justify-between`
- spacing from the default scale: `p-4`, `px-6`, `gap-3`, `mt-8`
- sizing helpers: `w-full`, `min-h-screen`
- simple typography: `text-sm`, `font-medium`, `leading-none`
- simple radii when generic: `rounded-full`, `rounded-xl`

Avoid arbitrary values in templates:

```vue
<!-- Avoid -->
<div class="px-[18px] text-[#111827] shadow-[0_8px_20px_rgba(15,23,42,0.04)]">
```

If a value is part of the visual identity or appears more than once, move it to tokens or component SCSS.

## SCSS modules

Prefer SCSS modules for component visuals:

```vue
<template>
  <section class="grid gap-4 p-4" :class="$style.card">
    ...
  </section>
</template>

<style module lang="scss">
.card {
  color: var(--color-text-primary);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}
</style>
```

Use SCSS modules for:

- colors
- component states
- custom shadows
- non-standard radii
- complex hover/active/focus styles
- component-specific responsive behavior
- styling that would otherwise require long Tailwind class strings

## Global styles

Global styles must stay minimal and should not define component classes.

Allowed global styles:

- Tailwind import
- font import or font-face declarations
- design tokens
- box sizing
- base `html`, `body`, `#app` styles
- inherited form control font styles

Avoid global selectors such as:

```scss
.button {}
.card {}
.catalog-filter {}
.modal {}
```

## Design tokens

Use a compact token set. Do not create a token for every component or pixel value.

Preferred token categories:

- primary color
- text colors
- surface colors
- border color
- a small number of shadows
- a small number of radii

Good examples:

```scss
--color-primary
--color-text-primary
--color-text-secondary
--color-surface
--color-surface-muted
--color-border
--shadow-card
--radius-card
```

Avoid over-specific tokens:

```scss
--catalog-filter-button-bg
--modal-title-color
--space-card-header-border-color
```

## `:deep(...)`

Avoid `:deep(...)` by default.

Use it only when:

- styling a third-party component that does not expose a better API
- styling generated markup that cannot be controlled directly

If `:deep(...)` is needed for internal components, prefer adding explicit props/classes to that component instead.

## Refactoring order

When refactoring existing styles, work in this order:

1. Introduce or reuse theme tokens.
2. Replace arbitrary Tailwind values with tokens or standard utilities.
3. Move component-specific visual styling into SCSS modules.
4. Remove unnecessary global styles and `:deep(...)` usage.
5. Verify the build after each meaningful area is completed.
