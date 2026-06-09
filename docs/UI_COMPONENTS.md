# UI Components (Base Kit)

The project ships a base component library in `frontend/src/components/common/`.
**Always reuse these components when building markup.** Do not hand-roll raw
`<input>`, `<button>`, chips, badges, or inline `<svg>` — use the kit so styling,
theming, and behavior stay consistent.

A live showcase of every component and state is available at the dev route **`/ui-kit`**
(`frontend/src/pages/UiKitPage.vue`).

All components are built on the design tokens in `frontend/src/styles/tokens.scss`
(`--color-primary`, `--color-surface`, `--radius-pill`, `--shadow-card`, ...) and
therefore re-theme automatically per tenant via `core/theme/apply-theme.ts`. Never
hardcode brand hex like `#2945ff` — use token utilities (`bg-primary`, `text-text-secondary`).

## Components

| Component | Use for | Key props |
| --- | --- | --- |
| `BaseButton` | Actions, filter pills | `tone` (`light`/`muted`/`white`/`clear`/`outline`), `active`, `size` (`xs`/`sm`/`md`/`lg`), `variant` (`pill`/`circle`), `type`, slots `#leading`/`#trailing` |
| `BaseIconButton` | Icon-only round buttons (favorite, close, menu) | `variant` (`surface`/`ghost`/`primary`), `size` (`sm`/`md`/`lg`), `active` |
| `BaseButtonGroup` | Segmented toggle | `v-model`, `options`, `size` |
| `BaseInput` | Text/search/tel inputs | `v-model`, `type`, `size`, `invalid`, `disabled`, `mask`, slots `#leading`/`#trailing` |
| `BaseTextarea` | Multi-line input | `v-model`, `rows`, `invalid`, `disabled` |
| `BaseField` | Label + hint + error wrapper | `label`, `hint`, `error`, `required` |
| `BaseSelect` → `BaseDropdown` | Dropdown / combobox | `v-model`, `options`, `placeholder`, `resetLabel` |
| `BaseCheckbox` | Checkbox | `v-model`, `disabled` |
| `BaseToggle` | Switch | `v-model`, `disabled` |
| `BaseChip` | Selectable / removable filter chip | `active`, `removable`, `size`, events `click`/`remove` |
| `BaseBadge` | Status labels on cards | `variant` (`neutral`/`primary`/`info`/`success`/`sale`), `size` |
| `RangeSlider` | Dual range (price/area/floor) | `min`, `max`, `minValue`, `maxValue`, `step`, `label`, `unit` |
| `BaseCard` | Surface container | `padding`, `interactive` |
| `BaseModal` | Modal shell | `panelClass`, `labelledBy`, event `close` |
| `BaseIcon` | All icons | `name`, `size` |

### Examples

```vue
<BaseButton active size="lg" type="submit">Забронировать</BaseButton>
<BaseButton tone="outline">Получить консультацию</BaseButton>

<BaseField label="Телефон">
  <BaseInput v-model="phone" type="tel" mask="+7 (###) ###-##-##" />
</BaseField>

<BaseChip :active="isActive" @click="select">Студия</BaseChip>
<BaseBadge variant="sale">-15%</BaseBadge>

<BaseIconButton variant="ghost" aria-label="Закрыть" @click="close">
  <BaseIcon name="close" :size="16" />
</BaseIconButton>
```

## Icons

Icons live as optimized, single-color SVGs in `frontend/src/assets/icons/*.svg`
(authored with `currentColor` so they inherit text color). They are imported as Vue
components via `vite-svg-loader` and rendered through `BaseIcon`.

**Never paste inline `<svg>` markup into components.** Add a new file to
`src/assets/icons/` and reference it by name:

```vue
<BaseIcon name="heart" :size="18" />
<BaseIcon name="chevron-down" :size="14" class="rotate-180" />
```

Available icons: `heart`, `heart-filled`, `chevron-down`, `check`, `close`, `plus`,
`plus-circle`, `search`, `share`, `trash`, `file`, `expand`, `menu`.

Add a new icon by dropping a `currentColor` SVG into `src/assets/icons/<name>.svg` —
it is auto-registered and immediately usable as `<BaseIcon name="<name>" />`.

> Exception: data-visualization SVGs that are not icons (e.g. the interactive plan
> overlay in `components/plans/PlanViewer.vue`) stay inline.

## Masked inputs

Phone and other masked fields use the [`maska`](https://beholdr.github.io/maska/)
directive, wired into `BaseInput` via the optional `mask` prop:

```vue
<BaseInput v-model="phone" type="tel" mask="+7 (###) ###-##-##" />
```
