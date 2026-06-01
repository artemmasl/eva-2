# EVA-2

## Overview

EVA-2 is a configurable real-estate catalog platform for developers.

The platform receives real-estate data from Allio feeds and renders customizable public storefronts where users can browse apartments and contact managers.

The system supports:
- multi-tenant architecture
- customizable themes
- public catalogs
- iframe embedding
- standalone domains
- admin panel
- AI-powered search and automation

---

## Main Goal

Provide developers with a fast and configurable public real-estate catalog.

---

## Main Users

### Developers
Configure catalog appearance and manage settings.

### Public Users
Browse apartments and contact managers.

---

## Data Source

Primary real-estate data comes from external feeds.

MVP can use mocked or demo feeds.

---

## Core Features

- apartment catalog
- filters
- search
- map
- apartment details
- contact manager
- theme configuration
- multi-tenant support

---

## Non Goals (MVP)

- no advanced CMS
- no drag-drop builder
- no visual editor
- no payments
- no booking engine
- no advanced analytics

---

## Tech Stack

### Frontend
- Vue 3
- Composition API
- TypeScript
- Vite
- Pinia

### Backend
- Python
- FastAPI
- MongoDB

---

## Design Source

Figma:
https://www.figma.com/design/vD27aThv585J1c2zF1fS75/Allio?node-id=1214-38367&p=f&t=NXWkeaRDhMAHufhh-0

---

## Architecture Style

Config-driven multi-tenant storefront platform.