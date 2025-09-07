import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ✅ Read API key from Railway environment variables
API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route("/")
def home():
    return "ESP32 OCR Relay is running!"

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        data = request.get_json()
        image_b64 = data.get("image")

        if not image_b64:
            return "No image provided", 400

        # ✅ Google Vision API request
        vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
        payload = {
            "requests": [
                {
                    "image": {"content": image_b64},
                    "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
                }
            ]
        }

        r = requests.post(vision_url, json=payload)
        result = r.json()

        # ✅ Extract text safely
        text = ""
        if "responses" in result and len(result["responses"]) > 0:
            res = result["responses"][0]
            if "fullTextAnnotation" in res:
                text = res["fullTextAnnotation"].get("text", "")
            elif "textAnnotations" in res and len(res["textAnnotations"]) > 0:
                text = res["textAnnotations"][0].get("description", "")

        if not text.strip():
            return "No text detected"

        # ✅ Return plain text (easy for ESP32)
        return text.strip()

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway auto-assigns PORT
    app.run(host="0.0.0.0", port=port)
