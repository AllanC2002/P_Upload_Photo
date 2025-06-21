import requests

# URLs
LOGIN_URL = "http://localhost:8080/login"
UPLOAD_URL = "http://localhost:8081/upload-photo"

# Login credentials
login_data = {
    "User_mail": "ascorread1",
    "password": "1234"
}

# 1. Login para obtener el token
login_response = requests.post(LOGIN_URL, json=login_data)
if login_response.status_code != 200:
    print("❌ Login failed:", login_response.status_code, login_response.text)
    exit()

token = login_response.json()["token"]
print("✅ Token obtenido:", token)

# 2. Cargar imagen y enviarla
headers = {
    "Authorization": f"Bearer {token}"
}

# Asegúrate de tener esta imagen en tu directorio
with open("test.png", "rb") as image_file:
    files = {
        "file": image_file
    }
    response = requests.post(UPLOAD_URL, headers=headers, files=files)

# 3. Resultado
print("📤 Upload response:")
print(response.status_code, response.json())
