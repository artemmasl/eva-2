# EVA-2

Config-driven multi-tenant real-estate storefront platform.

## Structure

```text
/frontend
/backend
/docs
```

## Frontend

```bash
npm install
npm run dev
```

Run from `frontend`.

## Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run from `backend`.
