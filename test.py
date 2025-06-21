import requests

BASE_URL = "http://localhost:8081/upload-photo"

# Autenticación
login_data = {
    "User_mail": "ascorread1",
    "password": "1234"
}

login_response = requests.post("http://localhost:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Login failed:", login_response.status_code, login_response.text)
    exit()

token = login_response.json()["token"]
print("Token:", token)

# Ruta de la imagen a subir
image_path = "test.png"  # .jpg .png  or .jpeg

with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    headers = {
        "Authorization": f"Bearer {token}"
    }

    upload_response = requests.post(BASE_URL, files=files, headers=headers)
    print("Upload response:")
    print(upload_response.status_code)
    print(upload_response.json())
