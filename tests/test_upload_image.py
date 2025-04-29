import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app


client = TestClient(app)


def create_test_image() -> bytes:
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


def test_image():
    return create_test_image()


def test_upload_image(test_image):
    files = {
        "file": ("test.png", test_image, "image/png")
    }

    params = {
        "top_k": 5
    }

    response = client.post("/image/upload", files=files, params=params)

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
