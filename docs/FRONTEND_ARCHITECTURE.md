# FRONTEND ARCHITECTURE

## Overview

Frontend architecture is based on:
- DDD
- Clean Architecture
- modular layered structure

Core business logic must be isolated from:
- UI
- framework code
- Vue components

---

# Layers

## Core

Core contains:
- entities
- use cases
- repositories
- aggregates
- value objects
- business logic

Core MUST NOT depend on:
- Vue
- Pinia
- UI components
- browser APIs

Core may only contain:
- TypeScript
- domain logic
- pure business rules

---

## UI Layer

UI layer contains:
- Vue components
- pages
- layouts
- composables
- stores

UI layer consumes:
- use cases
- entities
- services

UI must not implement business logic directly.

---

# Entities

Entities are the main business objects.

Entity characteristics:
- has id
- has lifecycle
- contains business logic
- frequently changes

Examples:
- Developer
- Building
- Space
- ThemeConfig

---

## Entity Structure

Each entity contains:

### Model
Contains:
- entity state
- validation
- business rules

Rules:
- state must not be mutated directly
- use methods/getters/setters

---

### Factory
Creates entity instances.

---

### Repository
Responsible only for data access.

Repository:
- performs API requests
- performs database requests
- does not contain business logic

---

### Use Cases

Business scenarios.

Use cases:
- orchestrate entities
- validate business rules
- use repositories

Use cases must not store state.

---

# Reference Entities

Simple reference entities:
- cities
- banks
- statuses

---

# Value Objects

Immutable data objects without lifecycle.

Examples:
- PhoneNumber
- Coordinates
- Price

---

# Aggregates

Aggregates orchestrate multiple entities.

Example:
- catalog
- chessboard
- filter system

Aggregates may contain:
- entities
- use cases

---

# Services

Services work with datasets that are not entities.

Examples:
- reporting
- filtering
- sorting

---

# Utilities

Reusable helper functions.

Utilities must not contain business logic.

---

# Constants

Global constants:
- storage names
- mappers
- app names

---

# Folder Structure

```text
/core
  /api
  /entities
  /reference-entities
  /value-objects
  /aggregates
  /services
  /utilities
  /constants
```

---

# API Layer

API layer contains:
- fetch wrappers
- request transformers
- response transformers

API layer adapts frontend requests to backend contracts.

---

# Important Rules

- business logic must stay inside core
- Vue components must stay thin
- repositories must not contain business logic
- use cases orchestrate scenarios
- entities own their state
- stores are orchestration only