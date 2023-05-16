import requests

url = "https://api.elevenlabs.io/v1/voices"

headers = {
  "Accept": "application/json",
  "xi-api-key": "52595903f763f2b4f5e0d520a225b018"
}

response = requests.get(url, headers=headers)

print(response.text)