import requests

BASE_URL = "http://13.219.191.189:8080/upload-photo"

login_data = {
    "User_mail": "allancorrea",
    "password": "1234"
}

login_response = requests.post("http://52.203.72.116:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Login failed:", login_response.status_code, login_response.text)
    exit()

token = login_response.json()["token"]
print("Token:", token)

image_path = "tests/test.png"  # .jpg .png  or .jpeg

with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    headers = {
        "Authorization": f"Bearer {token}"
    }

    upload_response = requests.post(BASE_URL, files=files, headers=headers)
    print("Upload response:")
    print(upload_response.status_code)
    print(upload_response.json())
