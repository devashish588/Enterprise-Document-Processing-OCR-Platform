# Backend Design Guide

The backend follows a layered FastAPI architecture:

- Routers validate HTTP requests and enforce auth.
- Services own business workflow.
- Repositories isolate SQLAlchemy access.
- Models define persistence.
- Schemas define API contracts.

The document pipeline is intentionally synchronous for the first runnable release. Move `DocumentService.ingest_bytes` behind a queue when upload latency becomes a measurable problem.

