# PROJECT PLAN

This document is the authoritative high-level plan for finishing EVA-2.
It describes the domain hierarchy, navigation, pages, the plan-markup model,
the admin boundary, and the task breakdown. Keep it in sync with reality.

---

## 1. Domain hierarchy

Confirmed hierarchy (each level belongs to the one above):

```text
Developer (tenant)
  └─ Complex (ЖК)
       └─ Building (Дом / Корпус)
            └─ Section (Подъезд)
                 └─ Floor (Этаж)
                      └─ Space (Квартира / Парковка / Кладовка / Коммерция)
```

Notes:
- **Developer == Tenant.** One deployment/domain serves ONE developer. It is not
  a marketplace. `/` shows all complexes of the resolved developer.
- **Complex (ЖК)** is a NEW entity. Previously `Building` conflated complex and
  building. We split them: `Complex` is the marketing/landing unit; `Building`
  is a physical дом/корпус inside a complex.
- **Section / Floor** can be lightweight (derived from spaces) but must be
  addressable for the chessboard and floor-plan screens.
- **Space** keeps the existing `stype` model: `flat | parking | storage |
  commercial`, plus `is_apartment` boolean. Tabs Квартиры / Парковки / Кладовки /
  Коммерция map to `stype` (Квартиры = flat).

---

## 2. Tenant (developer) resolution

- **Production:** resolve developer by request host / subdomain.
- **Development:** fall back to a single default demo developer via env
  (e.g. `DEFAULT_TENANT_SLUG`).
- The resolved developer provides `theme_config` (colors, logo, typography)
  applied globally on the storefront.

OPEN: exact prod resolution (subdomain vs custom domain table) — refine when
admin/feed sync is built. Not blocking for current work.

---

## 3. Navigation & routes

Developer level is implicit (the tenant). Routes nest by complex.

| Page | Route | Status |
| --- | --- | --- |
| All complexes — list | `/` | DONE |
| All complexes — map | `/?view=map` | DONE |
| Complex landing (обложка) | `/complex/:complexId` | DONE |
| Spaces — Планировки (default) | `/complex/:complexId/spaces` (`?view=plans`) | DONE |
| Spaces — Визуальный подбор | `/complex/:complexId/spaces?view=visual` | DONE |
| Building visualization / генплан | `/complex/:complexId/building/:buildingId` | DONE |
| Spaces — Шахматка | `/complex/:complexId/spaces?view=chess` | DONE |
| Floor plan (План этажа) | `/complex/:complexId/floor/:floorId` | DONE |
| Space details (Квартира детальная) | `/complex/:complexId/spaces/:id` | DONE |
| Favorites | `/favorites` | DONE |

View modes (Планировки / Визуальный подбор / Шахматка) live on ONE spaces route
switched by `?view=` query, preserving active filters across modes.

### Overlays (no dedicated route; query flag or store state)
- AI assistant (AI-помощник) — global overlay over any page.
- Side menu (Боковое меню) — developer contacts drawer.
- Callback request (Обратная связь) — modal form.
- Filters (Фильтр) — modal. DONE.
- Same-layout variants (Просмотр одинаковых планировок) — modal.

---

## 4. Pages — descriptions

### 4.1 All complexes — list (`/`)
Developer home. Grid of complex cards (photo, name, "N spaces for sale",
"from X ₽", district/metro). Some cards expand room stats on hover. Top-right
toggle `Список / На карте`. Simplified header (burger, phone, AI, favorites).
Figma: `Все ЖК застройщика — список`, `ЖК обложка — лендинг, ховер карточки`.

### 4.2 All complexes — map (`/?view=map`)
Same complexes on a city map with price markers.
Figma: `Все ЖК застройщика — карта`.

### 4.3 Complex landing (`/complex/:complexId`)
Marketing page for one complex: cover with name/address/status, quick search
form, gallery, infrastructure description, about block, district map, layout
preview, stats. Sticky `Шапка ЖК` cover with room stats (e.g. 128 studios,
84 one-room...) and sticky nav with tabs Квартиры / Парковки / Кладовки /
Коммерция. Header has long-name / tooltip / back-button / overflow states.
Figma: `ЖК обложка — лендинг`, `Шапка ЖК — статистика по комнатам`,
`Шапка ЖК + фильтр`, `Шапка — *`.

### 4.4 Spaces — Планировки (`/complex/:complexId/spaces`)
Grid of space cards with plan images, filters (collapsed/expanded), sorting,
"Группировать по планировке". View-mode switch. DONE (current CatalogPage).
Figma: `Планировки *`, `Планировки, группировка по планировкам`.

### 4.5 Spaces — Визуальный подбор (`?view=visual`)
3D render of the quarter. Circle markers with count of matching spaces per
building. Hover a building → card "Дом №N, сдача, N квартир по запросу →
Смотреть квартиры". Buildings without matches are dimmed.
Figma: `Визуальный подбор`, `…выбор дома, развернутая инфа`,
`…ховер дома без подходящих квартир`.

### 4.6 Building visualization / генплан (`/complex/:complexId/building/:buildingId`)
Render of the selected building, floors highlighted with space counts, "Генплан"
button to go back. Selecting a floor → floor plan.
Figma: `Визуализация — генплан`.

### 4.7 Spaces — Шахматка (`?view=chess`)
Matrix of spaces by floor/section, status colors (на продаже / бронь / продано /
не подходит). Cell sizes 30×30 / 40×40, hover info/image. Section pagination,
"План этажа" button.
Figma: `Шахматка *`.

### 4.8 Floor plan (`/complex/:complexId/floor/:floorId`)
Floor blueprint with spaces colored by status, section tabs, vertical floor
list (with space counts) on the left, hover on a space.
Figma: `План этажа, подъезды сверху` (+вариант 2), `План этажа, ховер на квартиру`.

### 4.9 Space details (`/complex/:complexId/spaces/:id`)
Apartment detail card. DONE (`SpaceDetailsPage.vue`). Update internal links to
nested route.
Figma: `Квартира детальная` (+ variants).

### 4.10 Favorites (`/favorites`)
Favorite collections, type filter, share/delete collection. DONE.

### 4.11 AI assistant (overlay)
Start screen + chat for guided search, with side panels showing space info /
map / complex. Figma: `AI старт`, `AI диалог + *`.

### 4.12 Side menu (overlay)
Developer contacts, socials, "Обратная связь" button. Partial (`SideMenu.vue`).
Figma: `Боковое меню`.

### 4.13 Callback request (overlay)
Callback form: "Перезвонить сейчас" / "Выбрать удобное время" with time slots.
Figma: `Обратная связь`.

### 4.14 Same-layout variants (overlay)
Modal listing variants of one layout by floor/price with tags.
Figma: `Просмотр одинаковых планировок`.

---

## 5. Plan markup model (for admin + storefront)

Interactive screens (визуальный подбор, генплан, шахматка, план этажа) render
clickable regions over images. Admin will later upload images and draw regions;
the storefront only renders from data. Design now so contracts are stable.

### Entities
- **PlanAsset** — an uploaded image to annotate.
  - `id`, `complex_id`, `kind` (`masterplan | building | floor`),
    `target_id` (building_id / floor_id), `image_url`, `width`, `height`.
- **PlanRegion** — one clickable polygon on a PlanAsset.
  - `id`, `asset_id`, `points` (array of normalized `[x, y]` in `0..1`),
    `target_kind` (`building | floor | space`), `target_id`,
    `label` (e.g. "Дом №3", "18 этаж"), `status` (mirrors space/aggregate status).

Storefront renders regions as SVG `<polygon>` overlays scaled to the rendered
image; status drives fill/opacity; click navigates to the target.

OPEN: whether floor `status` is stored or derived from contained spaces
(prefer derived for accuracy; allow override). Decide during backend task.

---

## 6. Admin boundary

### 6.1 Basic developers admin (DONE)
Multi-developer support + a basic admin panel are now built:

- **Developers in MongoDB.** New backend module `app/modules/developers`
  (Mongo collection `developers`, seeded on startup via FastAPI `lifespan` with
  demo `developer-1` "atlas" + `developer-2` "samolet"; `$setOnInsert` so admin
  edits survive restarts; graceful in-memory fallback when Mongo is down).
  Endpoints: `GET /api/developers` (admin), `GET /api/developers/by-slug/{slug}`
  (public), `GET /api/developers/{id}` (admin), `PUT /api/developers/{id}`
  (admin) editing basic info (name, slug, phone, logo) + `theme_config`.
- **Admin auth.** `app/modules/admin`: `POST /api/admin/login` checks
  `ADMIN_PASSWORD` (env, default `admin`) and returns a stateless bearer token
  (sha256 of salt+password); `require_admin` dependency guards developer writes.
- **Tenant resolution by slug.** `tenants` now builds the tenant from the
  developers repo: `GET /api/tenants/by-developer/{slug}`. `DeveloperSchema`
  moved to the developers module (tenants re-exports it).
- **Feed extended to a second developer.** `demo_feed.py` adds complex-3/4,
  building-3/4 and ~60 spaces for `developer-2`; `GET /api/complexes?developer=
  slug` filters by developer (slug resolved -> developer_id).
- **Path-based developer switching.** Storefront routes are nested under
  `/:developer` (`/atlas/...`, `/samolet/...`); `/` redirects to the default
  developer. `core/routing/storefront-link.ts` `useStorefrontLink()` injects the
  active `developer` param into every named storefront link; `AppLayout` loads
  the tenant via `tenantStore.loadTenantBySlug(route.params.developer)`.
- **Admin SPA.** `/admin/login` (password) + `/admin` (AdminLayout, guarded by
  `meta.requiresAdmin` + router `beforeEach`): developers list and an edit page
  (basic info + global styles with a live theme preview). Token persisted in
  localStorage (`useAdminStore`).

### 6.2 Future admin work (NOT built)
- Upload + annotate plan images (masterplan/building/floor markup).
- Manage feed settings / sync.
- Richer developer fields (domains, socials), auth hardening, per-complex theme
  overrides.

---

## 7. Task breakdown

### Epic A — Routing & layout migration (DONE)
- A1. Add `Complex` entity (frontend core + backend module + demo feed). DONE.
- A2. Restructure routes to `/complex/:complexId/...`; keep `/` for complex list. DONE.
- A3. Adapt `AppLayout` named views for complex-scoped vs developer-scoped pages. DONE
  (CatalogHeader `showTypeTabs` hidden on developer-scoped routes; type tabs only
  within a complex).
- A4. Update existing internal links (cards, details, favorites) to nested routes. DONE.

### Epic B — Developer level
- B1. All complexes — list page. DONE — `ComplexesPage` with cover, "N квартир в
  продаже" badge, "от X ₽", location line, and hover-revealed room-group stats
  table (backend `/api/complexes` returns aggregated `stats`). Covers are gradient
  placeholders (no complex image assets in feed yet); Список/На карте toggle is
  wired via `?view=map` (B2).
- B2. All complexes — map view. DONE — `?view=map` toggle on `ComplexesPage`
  renders `ComplexesMap.vue` (Yandex Maps JS API v2.1, key in
  `VITE_YANDEX_MAPS_API_KEY`). Price placemarks per complex -> click navigates to
  catalog; graceful fallback states (loading / no-key / error). Map provider
  decided: Yandex v2.1 (v3 needs a different key product).
- B3. Simplified developer header. DONE — `CatalogHeader` brand title + phone are
  now dynamic: developer name (from loaded tenant) on developer-scoped routes,
  current complex name on complex-scoped routes; type tabs already hidden off
  complex scope (A3); "Анонимно" replaced by gradient "AI-помощник" pill (opens
  nothing yet — overlay is E1). Tenant loaded globally in `AppLayout` via
  `useTenantStore.loadTenant(hostname)`; current complex tracked via new
  `useComplexStore`. Backend `DeveloperSchema`/demo TENANT gained `phone`.

### Epic C — Complex landing
- C1. Complex cover header with room stats (`Шапка ЖК`) + header states. DONE —
  route `complex-landing` at `/complex/:complexId` -> `ComplexLandingPage.vue`:
  gradient hero cover with logo mark, name, address, status pill, and room-stats
  row. Two header states: per-room-type counts (Квартир-студий / Однокомнатных /
  …) when >=2 flat groups, else "N Квартир разной планировки". CTA -> catalog.
  Backend `RoomGroupStatSchema` gained `count`; `GET /api/complexes/{id}` now
  returns `ComplexSummarySchema` (with stats). Complex cards + map placemarks now
  link to the landing (not straight to catalog). Hero image is a gradient
  placeholder (no complex assets yet).
- C2. Sticky tabs nav (Квартиры/Парковки/Кладовки/Коммерция). DONE — sticky
  space-type tab bar on `ComplexLandingPage`; each tab calls `catalogStore.setFilters`
  + pushes to `catalog` (mirrors header `changeSpaceType`).
- C3. Landing sections (gallery, about, infrastructure, district map, previews).
  DONE — sections on `ComplexLandingPage`: О проекте (text + facts grid),
  Галерея (gradient placeholder tiles — no real assets), Планировки квартир
  (cards from flat room-groups -> catalog filtered by rooms), Инфраструктура
  (static demo cards), Расположение (reuses `ComplexesMap` with the single complex).
  Marketing copy/infrastructure are demo placeholders (real content -> F2).

### Epic D — Spaces view modes
- D1. View-mode switch + `?view=` plumbing preserving filters. DONE — shared
  `src/core/catalog/views.ts` (CATALOG_VIEWS / resolveCatalogView); toolbar in
  `CatalogRouteTop` is now RouterLinks toggling `?view=` (plans = clean URL),
  filters/search live in the store so they persist across switches; `CatalogPage`
  renders `SpaceList` (plans) / `SpacesVisualView` / `SpacesChessView` by
  `activeView`. Visual & chess are placeholder components (D2/D4 will fill them).
  Infinite-scroll trigger re-observed when returning to plans view.
- D2. Визуальный подбор (masterplan render + building markers). DONE —
  reusable `src/components/plans/PlanViewer.vue` (SVG polygon overlays from
  normalized PlanRegion points, hover/selected/dimmed states). `SpacesVisualView`
  loads masterplan via getPlanWithRegions, renders building markers + side panel
  (Открыть корпус -> building-viz; Смотреть квартиры -> catalog filtered by
  building_id). Graceful empty fallback when no markup.
- D3. Building visualization (генплан, floor highlights). DONE — route
  `building-viz` /complex/:complexId/building/:buildingId -> `BuildingViewPage`
  (building plan + floor regions via PlanViewer; floor click -> floor-plan).
- D4. Шахматка (matrix, statuses, sections, sizes). DONE — `SpacesChessView`
  fetches all flats for the complex (getCatalogSpaces limit 1000, respects current
  catalog filters), groups by floor (rows desc), clickable cells -> space-details.
- D5. План этажа (blueprint, floor list, sections, hover). DONE — route
  `floor-plan` /complex/:complexId/floor/:floorId -> `FloorPlanPage` (floor plan +
  space regions via PlanViewer; space click -> space-details). Graceful fallback.

### Epic E — Overlays
- E1. AI assistant (start + chat). DONE — `AiAssistant.vue` left-docked panel
  (slide-in), opened from CatalogHeader "AI-помощник" pill (uiStore.openAi).
  Start screen (greeting + suggestion chips) + chat: user bubbles, assistant
  replies with real complex result cards (getComplexes, top 3 by price ->
  complex-landing) + follow-up chips; composer input + send; new-chat reset;
  ui.store isAiOpen/openAi/closeAi. UPDATED: replies are now powered by a real
  LLM (YandexGPT via OpenAI-compatible API) with streaming output. Backend
  module `app/modules/ai` (router `/api/ai/chat` SSE stream, `/api/ai/history`
  GET/DELETE) runs a function-calling loop with tools over spaces/complexes
  (search_spaces, list_complexes, get_space_details), injects page context
  (complex_id/name, space_id, page) into the system prompt, and persists chat
  history in MongoDB (`ai_conversations`) keyed by an httpOnly session cookie
  (`eva_ai_session`). Config: YANDEX_FOLDER_ID/YANDEX_API_KEY/YANDEX_MODEL.
  Frontend `ai.api.ts` consumes the SSE stream with credentials. The secondary
  detail/map side panel from figma is still not built.
- E2. Side menu (finish to match figma). DONE — `SideMenu.vue` title + sales phone
  now bound to tenant developer (developerName/salesPhone/salesPhoneHref);
  "Обратная связь" button opens callback modal (uiStore.openCallback).
- E3. Callback request modal. DONE — `CallbackModal.vue` (name+phone form, local
  success state, no backend) rendered globally in AppLayout; opened from SideMenu;
  ui.store isCallbackOpen/openCallback/closeCallback.
- E4. Same-layout variants modal. DONE — `SameLayoutModal.vue` rendered globally;
  opened from SpaceDetailsPage "Ещё N квартир с такой планировкой" link
  (uiStore.openSameLayout(space)). Fetches same complex+rooms via
  getAllCatalogSpaces, filters |area-ref|<=2, lists clickable rows -> space-details.
  ui.store isSameLayoutOpen/sameLayoutSpace/openSameLayout/closeSameLayout.

### Epic F — Data contracts
- F1. PlanAsset / PlanRegion schemas + demo data in feed. DONE — backend module
  `app/modules/plans` (PlanAssetSchema {id,complex_id,kind,target_id,image_url,
  width,height}; PlanRegionSchema {id,asset_id,points[[x,y]] normalized,
  target_kind,target_id,label,status}); endpoints GET /api/plans/assets
  (?complex_id&kind&target_id), /assets/{id}, /assets/{id}/regions. Demo data in
  `demo_feed.py` (masterplans for complex-1/2 -> building regions; building-1/2
  plans -> floor regions; floor plan -> space regions). Frontend entity
  `src/core/entities/plan` + `src/core/api/plans.api.ts` (getPlanWithRegions
  returns null when markup missing -> graceful). image_url empty (no assets);
  viewers render gradient placeholder + SVG region overlays.
- F2. Theme config consumption per developer. DONE — `src/core/theme/apply-theme.ts`
  `applyThemeConfig(theme)` overrides `:root` CSS vars (`--color-primary`,
  derived `--color-primary-hover`, `--app-font`); `AppLayout` applies it on tenant
  load (watch developer, immediate). `global.scss` font-family now uses
  `var(--app-font, 'Jost', sans-serif)`. `CatalogHeader` shows developer `logo`
  (brandLogo prop) when present, else the letter mark. Demo developer theme
  primaryColor `#1f6feb` (tenants repo).
- F3. Graceful fallbacks when markup is missing. DONE — `getPlanWithRegions`
  returns null when an asset/markup is missing; `SpacesVisualView`,
  `BuildingViewPage`, `FloorPlanPage` render empty states; `SpacesVisualView` &
  `SpacesChessView` empty states now include a "Перейти к планировкам" CTA
  (RouterLink -> `?view=plans`) so visual/chess fall back to the list. Theme
  degrades to default tokens when `theme_config` is empty (applyThemeConfig
  removes overrides). Plan viewers show a gradient placeholder when `image_url`
  is empty.

---

## 8. Open questions / decisions log
- Prod tenant resolution detail (subdomain vs domain table) — deferred.
- Floor status stored vs derived — DECIDED: derive floor/aggregate status from
  contained spaces (available if any contained space is available), with an
  optional explicit override field for admin. Storefront currently reads
  `PlanRegion.status` as-is (demo data sets it); the derive-vs-override logic
  lands with the admin/feed work, contract unchanged.
- Map provider for complex/district maps — TBD.
