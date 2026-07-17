# API Documentation

Base path: `/api/v1`

| Method | URL | Purpose | Auth |
| --- | --- | --- | --- |
| GET | `/health` | service health | none |
| POST | `/auth/register` | create user and token | none |
| POST | `/auth/login` | issue token | none |
| POST | `/documents` | upload and process document | bearer |
| GET | `/documents` | list documents | bearer |
| GET | `/documents/{id}` | document detail with OCR, fields, validation | bearer |
| GET | `/search?q=` | search OCR text and filenames | bearer |
| GET | `/reports/documents.csv` | export CSV | bearer |
| GET | `/analytics/summary` | dashboard aggregates | bearer |
| GET | `/audit-logs` | latest audit logs | admin bearer |

Request and response schemas are generated in Swagger at `/docs`.

## Status Codes

- `200`: successful read/export.
- `201`: created user or document.
- `400`: invalid upload.
- `401`: missing or invalid token.
- `403`: role denied.
- `404`: document not found.
- `422`: schema validation error.

