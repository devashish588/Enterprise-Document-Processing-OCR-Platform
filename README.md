# Enterprise Document Processing & OCR Platform

Offline intelligent document processing platform for ingesting business documents, extracting OCR text, classifying document type, extracting fields, validating results, indexing content, searching, and exporting reports.

## Stack

- Backend: FastAPI, SQLAlchemy, Alembic, SQLite by default, PostgreSQL-ready
- AI/OCR: Tesseract strategy, EasyOCR pluggable strategy, OpenCV preprocessing, sklearn TF-IDF search
- Frontend: React, TypeScript, React Query, React Router, Chart-ready UI
- DevOps: Docker, Compose, Nginx, GitHub Actions

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
$env:PYTHONPATH="."
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5180` if you use the checked-in dev script, or the URL Vite prints.

## Test

```bash
cd backend
$env:PYTHONPATH="."
pytest tests
```

## Docker

```bash
docker compose up --build
```

Frontend: `http://localhost:8080`  
Backend: `http://localhost:8000`

## Default Flow

1. Register/login from frontend or `POST /api/v1/auth/register`.
2. Upload a document at `POST /api/v1/documents`.
3. Backend preprocesses image, runs OCR, classifies text, extracts fields, validates, stores records, and writes audit logs.
4. Search with `GET /api/v1/search?q=...`.
5. Export CSV with `GET /api/v1/reports/documents.csv`.

## Documentation

- [SRS](docs/SRS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Pipelines](docs/PIPELINES.md)
- [Project Framework](docs/PROJECT_FRAMEWORK.md)
- [Database Design](docs/DATABASE_DESIGN.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Frontend Design](docs/FRONTEND_DESIGN.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [User Guide](docs/USER_GUIDE.md)
