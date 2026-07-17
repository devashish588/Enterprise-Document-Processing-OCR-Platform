# Project Framework

## Folder Structure

```text
backend/
  app/
    api/routers/       FastAPI route modules
    core/              config, security, logging
    db/                SQLAlchemy base and session
    models/            ORM models
    repositories/      database access boundary
    schemas/           Pydantic request/response models
    services/          OCR, classification, extraction, validation, search, reporting
  alembic/             database migrations
  tests/               backend pytest checks
frontend/
  src/api/             typed API client
  src/components/      reusable UI components
  src/pages/           route-level pages
docs/                  architecture and delivery documents
infra/nginx/           frontend Nginx config
sample_data/           local sample docs and classifier data
postman/               API collection
scripts/               training and maintenance scripts
```

## Modules

- `core.config`: environment-backed settings.
- `core.security`: password hashing and signed bearer tokens.
- `db.session`: SQLAlchemy engine/session provider.
- `models.document`: users, documents, OCR results, extracted fields, validation issues, audit logs.
- `repositories`: CRUD and query methods.
- `services.document_service`: orchestration for ingest pipeline.
- `services.preprocessing`: OpenCV image enhancement.
- `services.ocr`: Tesseract strategy and EasyOCR pluggable strategy.
- `services.classification`: lightweight local classifier.
- `services.extraction`: document-field rules.
- `services.validation`: required-field and confidence checks.
- `services.search`: SQL filtering plus TF-IDF ranking.
- `services.reporting`: CSV export.
- `api.routers`: auth, documents, search, reports, analytics, audit, health.

## Dependencies

- Required backend: FastAPI, SQLAlchemy, Alembic, Pydantic, python-multipart, sklearn.
- Optional runtime improvements: Tesseract binary, OpenCV, Pillow, pytesseract, EasyOCR.
- Frontend: React, TypeScript, React Query, React Router, lucide icons.

## Interfaces

OCR engines implement `OCRStrategy.extract(path)`. Repositories expose `get`, `list`, and `add`. Services depend on repositories and return ORM/Pydantic-compatible data.

