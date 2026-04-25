import requests

url = "http://127.0.0.1:8000/auth/refresh"
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjYsImV4cCI6MTc3Nzc0MjAzMn0.j-HhZnQxcQvKtDgaEtlgsO0VrMQRh9g-ZNiK9rM757I"}

response = requests.get(url, headers=headers)
print(response.json())