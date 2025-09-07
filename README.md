# ESP32 OCR Relay (Google Vision)

Relay server for ESP32 → Google Vision → ESP32.

## How to Deploy on Railway

1. Fork this repo.
2. Go to Railway → New Project → Deploy from GitHub.
3. Add environment variable:
   - Key: `GOOGLE_API_KEY`
   - Value: your Vision API key.
4. Deploy. Get public URL → use in ESP32 code.
