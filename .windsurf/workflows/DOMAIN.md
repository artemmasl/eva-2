# DOMAIN MODEL

## Developer

Represents a real-estate developer company.

Fields:
- id
- name
- slug
- logo
- domains
- theme_config

---

## Complex (ЖК)

Represents a residential complex (marketing/landing unit).

Hierarchy: Developer → Complex → Building → Section → Floor → Space.

Fields:
- id
- developer_id
- name
- address
- district
- coordinates
- status
- theme_overrides (optional)

---

## Building (Дом / Корпус)

Represents a physical building inside a complex.

Fields:
- id
- complex_id
- name
- coordinates

---

## Section (Подъезд)

Represents an entrance/section inside a building.

Fields:
- id
- building_id
- name

---

## Floor (Этаж)

Represents a floor inside a section/building.

Fields:
- id
- building_id
- section_id
- number
- space_count (derived)

---

## Space

Represents a real-estate unit.

IMPORTANT:
Always use the term "space".
Do not use:
- apartment
- unit
- flat

Fields:
- id
- complex_id
- building_id
- section_id
- floor
- stype (flat | parking | storage | commercial)
- is_apartment
- rooms
- area
- price
- status
- images

---

## Feed

External source of real-estate data.

---

## ThemeConfig

Visual configuration for tenant storefront.

---

## Tenant

Developer storefront instance.

---

## PlanAsset

An uploaded image to annotate for interactive selection screens
(masterplan / building render / floor blueprint).

Fields:
- id
- complex_id
- kind (masterplan | building | floor)
- target_id (building_id or floor_id)
- image_url
- width
- height

---

## PlanRegion

A clickable polygon drawn on a PlanAsset (created in the admin, rendered on the
storefront as an SVG overlay).

Fields:
- id
- asset_id
- points (array of normalized [x, y] in 0..1)
- target_kind (building | floor | space)
- target_id
- label
- status (mirrors space/aggregate status)