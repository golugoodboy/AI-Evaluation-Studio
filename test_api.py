import requests

url = "http://127.0.0.1:8000/rag/"
payload = {
  "document_id": "ab1d09b8-dd95-4cc2-a0b6-e42e705e3a33",
  "query": "What is this book about?"
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
