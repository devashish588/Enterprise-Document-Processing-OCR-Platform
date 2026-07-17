# Frontend Design Guide

## Navigation

Persistent sidebar:

- Dashboard
- Upload
- Search
- Reports

## Pages

- Dashboard: processing metrics and document table.
- Upload: file picker with immediate backend processing.
- Document Viewer: OCR text and extracted fields.
- Search: query input with ranked results and snippets.
- Reports: CSV export entry point.
- Login: local user registration/sign-in flow.

## UX States

- Loading: React Query pending state.
- Empty: dashboard table renders empty when no documents exist.
- Error: failed API requests surface as thrown query errors.
- Responsive: sidebar collapses above content on small screens.

## Theme

The UI uses restrained enterprise colors, dense tables, and simple panels. Dark/light theme toggles can be added when product settings require them.

