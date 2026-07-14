from fastapi.testclient import TestClient
from main import app, DUMMY_API_KEY

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_successful_payment():
    headers = {"X-API-Key": DUMMY_API_KEY}
    payload = {"user_id": "user_123", "amount": 50.0, "currency": "EUR"}
    
    response = client.post("/api/v1/payments", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
    assert "transaction_id" in response.json()

def test_unauthorized_payment():
    payload = {"user_id": "user_123", "amount": 50.0, "currency": "EUR"}
    response = client.post("/api/v1/payments", json=payload) 
    assert response.status_code == 401

def test_invalid_payment_amount():
    headers = {"X-API-Key": DUMMY_API_KEY}
    payload = {"user_id": "user_123", "amount": -10.0, "currency": "EUR"}
    
    response = client.post("/api/v1/payments", json=payload, headers=headers)
    assert response.status_code == 422 