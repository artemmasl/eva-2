# Деплой демо (VPS + Docker)

Всё приложение поднимается одной командой: `nginx` отдаёт собранный фронтенд
и проксирует `/api` + `/health` на бэкенд (FastAPI), рядом работает MongoDB.
Заход по `http://IP_СЕРВЕРА` — без домена. Один origin = AI-чат (cookie + SSE) работает без доп. настроек.

```
[браузер] -> :80 nginx (web) ──/──> статика (Vue dist)
                              └─/api─> backend:8000 (uvicorn) -> mongo:27017
```

## 1. Арендовать VPS

Подойдёт минимальный (2 vCPU / 2 GB RAM, Ubuntu 22.04/24.04):
- **Hetzner Cloud** (CX22, ~€4/мес) — дёшево и стабильно;
- **Timeweb Cloud** / **Selectel** / **Beget** — РФ, оплата картой РФ.

Запиши публичный IP и пароль/SSH-ключ.

## 2. Подключиться и поставить Docker

```bash
ssh root@IP_СЕРВЕРА

# Docker + compose plugin
curl -fsSL https://get.docker.com | sh
```

## 3. Залить проект на сервер

Вариант A — через git (если репозиторий доступен):
```bash
git clone <URL_РЕПО> eva-2
cd eva-2
```

Вариант B — скопировать с локальной машины (запускать локально):
```bash
rsync -az --exclude node_modules --exclude .venv --exclude dist \
  ./ root@IP_СЕРВЕРА:/root/eva-2/
```

## 4. Настроить переменные окружения

```bash
cd eva-2
cp .env.production.example .env
nano .env
```
Обязательно:
- `ADMIN_PASSWORD` — поставь свой (вход в `/admin`);
- `CORS_ORIGINS=http://IP_СЕРВЕРА`;
- `YANDEX_FOLDER_ID` + `YANDEX_API_KEY` — если нужен AI-чат (иначе оставь пустыми, чат просто будет недоступен).

## 5. Собрать и запустить

```bash
docker compose up -d --build
```

Проверка:
```bash
docker compose ps
curl http://localhost/health      # {"status":"ok"}
```

Открой в браузере: `http://IP_СЕРВЕРА`

## 6. Обновление демо

```bash
git pull            # или повторный rsync
docker compose up -d --build
```

## Полезное

```bash
docker compose logs -f backend     # логи бэка
docker compose logs -f web         # логи nginx
docker compose down                # остановить (данные mongo сохранятся в volume)
docker compose down -v             # остановить и стереть данные mongo
```

## Заметки

- **Данные.** Демо-застройщики и фид сидируются на старте бэкенда; правки в `/admin`
  и AI-сессии хранятся в Mongo (volume `mongo_data`). При `down -v` всё сбрасывается.
- **HTTPS.** Для демо по IP не обязателен. Если позже появится домен — можно
  добавить Caddy/Traefik или certbot перед `web`.
- **Файрвол.** Открой порт 80: `ufw allow 80 && ufw allow OpenSSH && ufw enable`.
