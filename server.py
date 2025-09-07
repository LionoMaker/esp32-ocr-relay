from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Read API key from environment variable (secure way)
API_KEY = os.getenv("GOOGLE_API_KEY")
#API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route("/")
def home():
    return "ESP32 OCR Relay is running!"

@app.route("/ocr", methods=["POST"])
def ocr():
    data = request.json
    image_content = data.get("image")
    if not image_content:
        return jsonify({"error": "No image data"}), 400

    vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
    payload = {
        "requests": [{
            "image": {"content": image_content},
            "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
        }]
    }

    r = requests.post(vision_url, json=payload)
    result = r.json()

    # Extract only text
    text = ""
    try:
        text = result["responses"][0]["fullTextAnnotation"]["text"]
    except:
        text = "No text detected"

    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
