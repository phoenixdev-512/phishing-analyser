import requests
import time

try:
    print("Sending request...")
    response = requests.post("http://localhost:8000/api/analyze", json={"url": "https://google.com"})
    print(response.status_code)
    print(response.json().get("ai_analysis"))
except Exception as e:
    print(e)
