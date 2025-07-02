import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    from main import app
    app.config['TESTING'] = True
    return app.test_client()

def test_upload_photo_success(client):
    mock_token = "mocktoken"
    mock_user_id = "user123"

    with patch("main.jwt.decode") as mock_jwt_decode, \
         patch("services.functions.conection_mongo") as mock_conection_mongo:

        mock_jwt_decode.return_value = {"user_id": mock_user_id}

        mock_db = MagicMock()
        mock_images_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_images_collection
        mock_conection_mongo.return_value = mock_db

        with open("tests/test.png", "rb") as img_file:
            response = client.post(
                "/upload-photo",
                headers={"Authorization": f"Bearer {mock_token}"},
                content_type="multipart/form-data",
                data={"file": (img_file, "test.png")}
            )

        assert response.status_code == 201
        assert response.json["message"] == "Image uploaded successfully"
