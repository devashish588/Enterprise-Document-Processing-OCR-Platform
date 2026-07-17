# Testing Guide

## Backend

```bash
cd backend
pip install -r requirements-dev.txt
$env:PYTHONPATH="."
pytest tests
```

The smoke test registers an admin, uploads a sample invoice text document, verifies OCR/classification/extraction/search, and downloads CSV.

## Frontend

```bash
cd frontend
npm install
npm run build
```

## API

Import `postman/Enterprise-Document-Processing.postman_collection.json`.

## Future Test Growth

- Add OCR accuracy fixtures for real scanned images.
- Add RBAC negative-path tests.
- Add frontend component tests when UI behavior stabilizes.
- Add load tests after a worker queue exists.

