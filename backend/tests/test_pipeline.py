import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient

from app.main import create_app


def test_document_pipeline_upload_search_and_report(tmp_path):
    client = TestClient(create_app())
    token = client.post("/api/v1/auth/register", json={"email": "admin@example.com", "password": "secret123", "role": "admin"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    invoice_text = b"Invoice Number INV-1001\nDate 17/07/2026\nGST 27ABCDE1234F1Z5\nTotal Rs. 1250.00\n"
    upload = client.post("/api/v1/documents", files={"file": ("invoice.txt", invoice_text, "text/plain")}, headers=headers)
    assert upload.status_code == 201
    assert upload.json()["document_type"] == "invoice"

    detail = client.get(f"/api/v1/documents/{upload.json()['id']}", headers=headers)
    assert detail.status_code == 200
    assert any(field["name"] == "invoice_number" for field in detail.json()["fields"])

    search = client.get("/api/v1/search?q=INV-1001", headers=headers)
    assert search.status_code == 200
    assert search.json()[0]["document"]["filename"] == "invoice.txt"

    report = client.get("/api/v1/reports/documents.csv", headers=headers)
    assert report.status_code == 200
    assert "invoice.txt" in report.text

