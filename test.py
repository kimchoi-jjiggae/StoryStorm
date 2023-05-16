import requests

# streaming chunk size
CHUNK_SIZE = 1024

XI_API_KEY = "52595903f763f2b4f5e0d520a225b018"


url = "https://api.elevenlabs.io/v1/text-to-speech/W9AqZKoLZscRHWjcPSkk"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": XI_API_KEY
}

data = {
  "text": "Some very long text to be read by the voice",
  "voice_settings": {
    "stability": 0,
    "similarity_boost": 0
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
