# System Architecture

## System Context

```mermaid
flowchart LR
  User["Admin / Analyst / Auditor"] --> UI["React Frontend"]
  UI --> API["FastAPI Backend"]
  API --> DB[("SQL Database")]
  API --> Storage["Local Document Storage"]
  API --> OCR["Local OCR Engines"]
  API --> Search["SQL + TF-IDF Search"]
```

## Enterprise Architecture

```mermaid
flowchart TB
  Presentation["Presentation Layer: React"] --> API["API Layer: FastAPI Routers"]
  API --> Services["Service Layer: OCR, Classification, Extraction, Validation, Search, Reporting"]
  Services --> Repos["Repository Layer"]
  Repos --> Data["SQLAlchemy Models + Database"]
  Services --> Files["Document Storage"]
  Services --> Observability["Logging + Audit Logs"]
```

## Component Diagram

```mermaid
flowchart LR
  Auth["Auth/RBAC"] --> Routers
  Routers --> DocumentService
  DocumentService --> Preprocess["ImagePreprocessor"]
  DocumentService --> OCREngine
  DocumentService --> Classifier
  DocumentService --> Extractor
  DocumentService --> Validator
  DocumentService --> Repositories
  SearchRouter --> SearchEngine
  ReportsRouter --> ReportingService
```

## Deployment Diagram

```mermaid
flowchart LR
  Browser --> Nginx["Nginx + React Static Assets"]
  Browser --> FastAPI["FastAPI Container"]
  FastAPI --> Volume["Storage Volume"]
  FastAPI --> SQLite[("SQLite / PostgreSQL")]
```

## Sequence Diagram

```mermaid
sequenceDiagram
  participant U as User
  participant F as Frontend
  participant A as FastAPI
  participant S as DocumentService
  participant D as Database
  U->>F: Upload document
  F->>A: POST /documents
  A->>S: ingest bytes
  S->>S: preprocess, OCR, classify, extract, validate
  S->>D: save document, OCR, fields, issues, audit
  A-->>F: document summary
  F-->>U: processing result
```

## Security Architecture

- Passwords use PBKDF2-HMAC-SHA256.
- Tokens use compact HS256 JWT-compatible bearer tokens.
- RBAC is enforced through FastAPI dependencies.
- SQL injection protection is provided by SQLAlchemy parameterization.
- CORS origins are environment controlled.
- File scanning is a hook point before storage in `DocumentService.ingest_bytes`.
- Audit logs capture user activity.

## Scalability And Recovery

- Switch `DATABASE_URL` from SQLite to PostgreSQL for concurrent production use.
- Move storage path to shared volume or object storage when cloud deployment is required.
- Replace in-process OCR with a queue worker when throughput requires it.
- Use Alembic migrations for repeatable schema rollout.
- Back up SQL database and upload storage together.

## Monitoring

- API logs are structured through Python logging.
- Audit logs persist business actions.
- Add Prometheus/OpenTelemetry when there is a real runtime target.

