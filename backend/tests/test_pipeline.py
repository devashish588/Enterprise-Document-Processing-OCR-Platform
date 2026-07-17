import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ALLOWED_ORIGINS"] = "http://127.0.0.1:5180,http://localhost:5180"

from fastapi.testclient import TestClient
import pytest

from app.core.config import get_settings
get_settings.cache_clear()

from app.main import create_app

INVOICE = b"Invoice Number INV-1001\nDate 17/07/2026\nGST 27ABCDE1234F1Z5\nTotal Rs. 1250.00\n"
RECEIPT = b"Receipt\nCash paid 500\nChange 50\nTotal 450\n"


@pytest.fixture(scope="module")
def client():
    return TestClient(create_app())


@pytest.fixture(scope="module")
def auth_headers(client):
    token = client.post(
        "/api/v1/auth/register",
        json={"email": "admin@example.com", "password": "secret123", "role": "admin"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["database"] == "ok"


def test_cors_preflight(client):
    r = client.options(
        "/api/v1/documents",
        headers={
            "Origin": "http://127.0.0.1:5180",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == "http://127.0.0.1:5180"


def test_register_duplicate_returns_409(client):
    client.post("/api/v1/auth/register", json={"email": "dup@example.com", "password": "pw"})
    r = client.post("/api/v1/auth/register", json={"email": "dup@example.com", "password": "pw"})
    assert r.status_code == 409


def test_login_invalid_credentials(client):
    r = client.post("/api/v1/auth/login", json={"email": "nobody@example.com", "password": "wrong"})
    assert r.status_code == 401


def test_protected_endpoint_without_token(client):
    r = client.get("/api/v1/documents")
    assert r.status_code == 401


def test_invoice_pipeline(client, auth_headers):
    r = client.post("/api/v1/documents", files={"file": ("invoice.txt", INVOICE, "text/plain")}, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["document_type"] == "invoice"
    assert data["confidence"] > 0

    detail = client.get(f"/api/v1/documents/{data['id']}", headers=auth_headers)
    assert detail.status_code == 200
    fields = {f["name"] for f in detail.json()["fields"]}
    assert "invoice_number" in fields
    assert "gst" in fields
    assert "total_amount" in fields


def test_receipt_pipeline(client, auth_headers):
    r = client.post("/api/v1/documents", files={"file": ("receipt.txt", RECEIPT, "text/plain")}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["document_type"] == "receipt"


def test_document_not_found(client, auth_headers):
    r = client.get("/api/v1/documents/99999", headers=auth_headers)
    assert r.status_code == 404


def test_list_documents_pagination(client, auth_headers):
    r = client.get("/api/v1/documents?limit=1&offset=0", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) <= 1


def test_list_documents_filter_by_type(client, auth_headers):
    r = client.get("/api/v1/documents?document_type=invoice", headers=auth_headers)
    assert r.status_code == 200
    for doc in r.json():
        assert doc["document_type"] == "invoice"


def test_search(client, auth_headers):
    r = client.get("/api/v1/search?q=INV-1001", headers=auth_headers)
    assert r.status_code == 200
    assert any(hit["document"]["filename"] == "invoice.txt" for hit in r.json())


def test_analytics_summary(client, auth_headers):
    r = client.get("/api/v1/analytics/summary", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert "total" in data
    assert "by_type" in data
    assert "by_status" in data
    assert "avg_confidence" in data
    assert "daily_trend" in data


def test_csv_report(client, auth_headers):
    r = client.get("/api/v1/reports/documents.csv", headers=auth_headers)
    assert r.status_code == 200
    assert "invoice.txt" in r.text


def test_excel_report(client, auth_headers):
    r = client.get("/api/v1/reports/documents.xlsx", headers=auth_headers)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/vnd.openxmlformats")


def test_delete_document(client, auth_headers):
    upload = client.post("/api/v1/documents", files={"file": ("del.txt", b"invoice total 100", "text/plain")}, headers=auth_headers)
    doc_id = upload.json()["id"]
    r = client.delete(f"/api/v1/documents/{doc_id}", headers=auth_headers)
    assert r.status_code == 204
    assert client.get(f"/api/v1/documents/{doc_id}", headers=auth_headers).status_code == 404


def test_audit_logs_require_admin(client):
    token = client.post(
        "/api/v1/auth/register",
        json={"email": "analyst@example.com", "password": "pw", "role": "analyst"},
    ).json()["access_token"]
    r = client.get("/api/v1/audit-logs", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403


def test_audit_logs_admin_access(client, auth_headers):
    r = client.get("/api/v1/audit-logs", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_me_endpoint(client, auth_headers):
    r = client.get("/api/v1/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "admin@example.com"
    assert r.json()["role"] == "admin"


def test_empty_file_rejected(client, auth_headers):
    r = client.post("/api/v1/documents", files={"file": ("empty.txt", b"", "text/plain")}, headers=auth_headers)
    assert r.status_code == 400
