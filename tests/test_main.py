import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from database import get_session
from main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_ping(client: TestClient):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_crud_links(client: TestClient):
    # 1. Create link
    payload = {
        "original_url": "https://example.com/long-url",
        "short_name": "exmpl",
    }
    response = client.post("/api/links", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["original_url"] == payload["original_url"]
    assert data["short_name"] == payload["short_name"]
    assert "short_url" in data

    # 2. Get list of links
    response = client.get("/api/links")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 3. Get link by ID
    response = client.get("/api/links/1")
    assert response.status_code == 200
    assert response.json()["short_name"] == "exmpl"

    # 4. Redirect
    response = client.get("/r/exmpl", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/long-url"

    # 5. Update link
    update_payload = {
        "original_url": "https://example.com/new-url",
        "short_name": "exmpl_new",
    }
    response = client.put("/api/links/1", json=update_payload)
    assert response.status_code == 200
    assert response.json()["short_name"] == "exmpl_new"

    # 6. Delete link
    response = client.delete("/api/links/1")
    assert response.status_code == 204

    # 7. Check 404 after delete
    response = client.get("/api/links/1")
    assert response.status_code == 404