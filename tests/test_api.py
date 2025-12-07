"""API smoke tests using FastAPI TestClient."""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_text():
    payload = {"text": "This synthetic post claims 100% success so you must act immediately."}
    response = client.post("/analyze_text", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert "linguistic" in data
    assert "misinformation" in data


def test_analyze_text_rejects_whitespace_only():
    response = client.post("/analyze_text", json={"text": "   "})
    assert response.status_code == 422


def test_analyze_image():
    # create simple base64 png
    import base64
    import io

    from PIL import Image

    img = Image.new("RGB", (4, 4), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()

    payload = {"image_b64": encoded}
    response = client.post("/analyze_image", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "vector_representation" in body
    assert body["metadata"]["source"] == "image"


def test_analyze_image_rejects_invalid_base64():
    response = client.post("/analyze_image", json={"image_b64": "not-base64"})
    assert response.status_code == 422


def test_analyze_url():
    payload = {"url": "https://synthetic.invalid/post"}
    response = client.post("/analyze_url", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "clean_text" in body
    assert body["metadata"]["status"] == "simulated"


def test_risk_score():
    payload = {
        "text_items": ["Synthetic urgent message", "Harmless fictional update"],
        "domain_credibility": 70,
    }
    response = client.post("/risk_score", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "risk" in body and "level" in body["risk"]
