import requests
import base64
import json
import os
from PIL import Image

# Step 1: Convert image to RGB JPEG to avoid format issues
image_path = r"C:\Users\navir\OneDrive\Desktop\Katana_ai\serpscrape\product_image.jpg"
converted_path = r"C:\Users\navir\OneDrive\Desktop\Katana_ai\serpscrape\converted_image.jpg"

# Convert image to RGB to ensure compatibility
try:
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.save(converted_path, "JPEG")
except Exception as e:
    print(f"Image conversion failed: {e}")
    exit(1)

# Step 2: Load and encode image in base64
try:
    with open(converted_path, "rb") as f:
        image_bytes = f.read()
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
except Exception as e:
    print(f"Image loading/encoding failed: {e}")
    exit(1)

# Step 3: Send request to local Ollama LLaVA endpoint
try:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llava",
            "messages": [
                {
                    "role": "user",
                    "content": "Describe this image.",
                    "images": [encoded_image]
                }
            ]
        },
        stream=True
    )
except Exception as e:
    print(f"Failed to reach Ollama API: {e}")
    exit(1)

# Step 4: Handle response stream
if response.status_code == 200:
    print("Response stream:")
    output = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                print("\n[DEBUG] Raw Line:", data)  # Optional: for debugging

                if "message" in data and "content" in data["message"]:
                    output += data["message"]["content"]
                elif "response" in data:
                    output += data["response"]
                elif "error" in data:
                    print(f"\n[ERROR]: {data['error']}")
            except json.JSONDecodeError as e:
                print(f"\n[ERROR] JSON decoding failed: {e}")
    print("\n\nFinal Output:\n", output)
else:
    print(f"[ERROR] HTTP {response.status_code}:\n{response.text}")
