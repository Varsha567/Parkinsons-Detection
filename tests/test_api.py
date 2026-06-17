from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_predict():

    payload = {
        "features": [
            119.992,
            157.302,
            74.997,
            0.00784,
            0.00007,
            0.00370,
            0.00554,
            0.01109,
            0.04374,
            0.426,
            0.02182,
            0.03130,
            0.02971,
            0.06545,
            0.02211,
            21.033,
            0.414783,
            0.815285,
            -4.813031,
            0.266482,
            2.301442,
            0.284654
        ]
    }

    response = client.post(
        "/predict",
        json=payload
    )

    assert response.status_code == 200
    assert "prediction" in response.json()