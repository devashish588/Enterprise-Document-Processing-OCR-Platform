# Database Design

## ER Diagram

```mermaid
erDiagram
  USERS ||--o{ DOCUMENTS : uploads
  DOCUMENTS ||--|| OCR_RESULTS : has
  DOCUMENTS ||--o{ EXTRACTED_FIELDS : has
  DOCUMENTS ||--o{ VALIDATION_ISSUES : has
  DOCUMENTS ||--o{ AUDIT_LOGS : references

  USERS {
    int id PK
    string email UK
    string password_hash
    string role
    datetime created_at
  }
  DOCUMENTS {
    int id PK
    string filename
    string content_type
    string storage_path
    string document_type
    string status
    float confidence
    int uploaded_by_id FK
    datetime created_at
  }
  OCR_RESULTS {
    int id PK
    int document_id FK
    string engine
    text text
    float confidence
    datetime created_at
  }
  EXTRACTED_FIELDS {
    int id PK
    int document_id FK
    string name
    text value
    float confidence
  }
  VALIDATION_ISSUES {
    int id PK
    int document_id FK
    string field_name
    string severity
    string message
  }
  AUDIT_LOGS {
    int id PK
    string actor
    string action
    string entity_type
    string entity_id
    text details
    datetime created_at
  }
```

## Normalization

Document metadata, OCR text, extracted fields, validation issues, users, and audit logs are separate tables. This keeps one-to-many extraction and validation data queryable without JSON-only storage.

## Indexes

- `users.email` unique index.
- `documents.document_type`, `documents.status`, `documents.created_at`.
- `extracted_fields.document_id`, `extracted_fields.name`.
- `validation_issues.document_id`.
- `audit_logs.actor`, `audit_logs.action`, `audit_logs.created_at`.

## Storage Strategy

Binary files live in local storage under `UPLOAD_DIR`. Database rows store metadata and storage path. This keeps the database portable and avoids large BLOB churn.

## Search Strategy

Current search combines SQL text filtering with TF-IDF ranking. PostgreSQL FTS or FAISS can replace the ranking layer when document volume justifies it.

## Migration Strategy

Alembic revision `0001_initial_schema.py` creates the initial normalized schema. Future changes add forward-only revisions.

