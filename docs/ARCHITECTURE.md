# FRONTEND

Frontend uses layered DDD-inspired architecture.

Core business logic is isolated from UI and framework code.

Business entities, repositories, use cases and aggregates are implemented inside the core layer.

Vue components must not contain business logic.