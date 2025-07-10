import requests

url = "http://127.0.0.1:5000/"
username = "admin"
passwords = ["1234", "admin", "password123"]

for pwd in passwords:
    response = requests.post(url, data={"username": username, "password": pwd})
    if "Login successful" in response.text:
        print(f"✅ Found password: {pwd}")
        break
    else:
        print(f" Tried: {pwd}")
