# Processing Pipelines

## OCR Pipeline

```mermaid
flowchart LR
  Upload --> Store --> Preprocess --> OCR["Tesseract / EasyOCR Strategy"] --> Confidence --> Persist
```

## Image Processing Pipeline

```mermaid
flowchart LR
  Image --> Grayscale --> Denoise --> Equalize --> Threshold --> ProcessedImage
```

## Classification Pipeline

```mermaid
flowchart LR
  Text --> Features["Keyword / TF-IDF features"] --> Classifier --> Label --> Confidence
```

## Field Extraction Pipeline

```mermaid
flowchart LR
  Text --> DocType --> RegexRules --> Fields --> FieldConfidence
```

## Validation Pipeline

```mermaid
flowchart LR
  Fields --> RequiredRules --> ConfidenceRules --> Issues --> ReviewStatus
```

## Storage Pipeline

```mermaid
flowchart LR
  File --> LocalStorage
  Metadata --> DocumentsTable
  OCR --> OCRTable
  Fields --> FieldsTable
  Issues --> ValidationTable
```

## Search Pipeline

```mermaid
flowchart LR
  Query --> SQLFilter --> TFIDFRanking --> Results --> Snippets
```

## Analytics Pipeline

```mermaid
flowchart LR
  Documents --> Aggregations --> SummaryAPI --> Dashboard
```

## Notification Pipeline

```mermaid
flowchart LR
  Event --> AuditLog
  Event --> ReviewQueue["Manual review queue"]
```

## Authentication Flow

```mermaid
flowchart LR
  Credentials --> VerifyPassword --> Token --> BearerHeader --> RBACDependency --> Route
```

