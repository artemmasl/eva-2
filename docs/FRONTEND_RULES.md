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

# Styling Rules

- Tailwind utility classes are preferred over local styles
- avoid global styles
- avoid :deep(...) unless absolutely necessary
- prefer explicit class styling
- avoid style leakage between components