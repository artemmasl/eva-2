# FRONTEND RULES

- Vue 3 only
- Composition API only
- script setup only
- TypeScript required
- Pinia only
- no Vuex
- use const fn = () => {}
- stores located in src/stores/modules
- composables located in src/composables
- avoid business logic inside components
- prefer typed interfaces
- reusable composables

# Base Components (MANDATORY)

- a base UI kit lives in `src/components/common/` — see `docs/UI_COMPONENTS.md` and the `/ui-kit` page
- ALWAYS reuse kit components when building markup: `BaseButton`, `BaseIconButton`, `BaseButtonGroup`, `BaseInput`, `BaseTextarea`, `BaseField`, `BaseDropdown`, `BaseCheckbox`, `BaseToggle`, `BaseChip`, `BaseBadge`, `RangeSlider`, `BaseCard`, `BaseModal`, `BaseIcon`
- never hand-roll raw `<input>`, `<button>`, chips or badges if a kit component exists
- never paste inline `<svg>` — add a `currentColor` SVG to `src/assets/icons/` and render via `<BaseIcon name="..." />`
- masked inputs use `BaseInput`'s `mask` prop (powered by `maska`)
- use design-token utilities (`bg-primary`, `text-text-secondary`, `rounded-pill`), never hardcoded brand hex

# Styling Rules

- Tailwind utility classes are preferred over local styles
- avoid global styles
- avoid :deep(...) unless absolutely necessary
- prefer explicit class styling
- avoid style leakage between components