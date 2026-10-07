from fastapi.testclient import TestClient

from jobastra_ai.core.config import get_settings


def test_health_check(monkeypatch) -> None:
    monkeypatch.setenv("DEBUG", "false")
    get_settings.cache_clear()

    from jobastra_ai.main import app

    client = TestClient(app)
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "jobastra-ai",
    }
