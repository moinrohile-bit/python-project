#!/usr/bin/env python3
# Object Detection using Hugging Face API
# Install: pip install pillow requests

import os
import io
import time
import random
import requests
import mimetypes
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ==============================
# ADD YOUR API KEY HERE
# ==============================
HF_API_KEY = "add api here"

# Model
MODEL = "facebook/detr-resnet-101"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"

# Settings
ALLOWED = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}
MAX_MB = 8

# Emojis for labels
EMOJI = {
    "person": "🧍", "car": "🚗", "truck": "🚚", "bus": "🚌",
    "bicycle": "🚲", "motorcycle": "🏍️", "dog": "🐶", "cat": "🐱",
    "bird": "🐦", "horse": "🐴", "sheep": "🐑", "cow": "🐮",
    "bear": "🐻", "giraffe": "🦒", "zebra": "🦓", "banana": "🍌",
    "apple": "🍎", "orange": "🍊", "pizza": "🍕", "broccoli": "🥦",
    "book": "📘", "laptop": "💻", "tv": "📺", "bottle": "🧴", "cup": "🥤"
}


# Load font
def load_font(size=18):
    for f in ("DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()


# Ask user for image
def ask_image():
    print("\n🎯 Select an image (JPG/PNG/WebP/BMP/TIFF ≤ 8MB)")
    while True:
        path = input("Image path: ").strip().strip('"').strip("'")

        if not path or not os.path.isfile(path):
            print("⚠️ File not found.")
            continue

        ext = os.path.splitext(path)[1].lower()
        if ext not in ALLOWED:
            print("⚠️ Unsupported format.")
            continue

        if os.path.getsize(path) / (1024 * 1024) > MAX_MB:
            print("⚠️ File too large (>8MB).")
            continue

        try:
            Image.open(path).verify()
        except:
            print("⚠️ Invalid image.")
            continue

        return path


# API inference
def detect_objects(path, img_bytes, retries=8):
    mime, _ = mimetypes.guess_type(path)

    for _ in range(retries):
        if mime and mime.startswith("image/"):
            response = requests.post(
                API,
                headers={
                    "Authorization": f"Bearer {HF_API_KEY}",
                    "Content-Type": mime
                },
                data=img_bytes,
                timeout=60
            )
        else:
            response = requests.post(
                API,
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                files={
                    "inputs": (
                        os.path.basename(path),
                        img_bytes,
                        "application/octet-stream"
                    )
                },
                timeout=60
            )

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and "error" in result:
                raise RuntimeError(result["error"])
            if not isinstance(result, list):
                raise RuntimeError("Unexpected API response.")
            return result

        if response.status_code == 503:
            print("⏳ Model warming up...")
            time.sleep(2)
            continue

        raise RuntimeError(
            f"API Error {response.status_code}: {response.text[:300]}"
        )

    raise RuntimeError("Model warm-up timeout.")


# Draw boxes
def annotate_image(img, detections, threshold=0.5):
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    counts = {}

    for det in detections[:50]:
        score = float(det.get("score", 0))
        if score < threshold:
            continue

        label = det.get("label", "object")
        box = det.get("box", {})

        x1 = int(box.get("xmin", 0))
        y1 = int(box.get("ymin", 0))
        x2 = int(box.get("xmax", 0))
        y2 = int(box.get("ymax", 0))

        if not (x2 > 0 and y2 > 0):
            x = int(box.get("x", 0))
            y = int(box.get("y", 0))
            w = int(box.get("w", 0))
            h = int(box.get("h", 0))
            x1, y1, x2, y2 = x, y, x + w, y + h

        color = tuple(random.randint(80, 255) for _ in range(3))

        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=4)

        text = f"{EMOJI.get(label.lower(), '✨')} {label} {score*100:.0f}%"
        text_width = draw.textlength(text, font=font)
        text_height = font.size + 6

        draw.rectangle(
            [(x1, max(0, y1 - text_height)), (x1 + text_width + 8, y1)],
            fill=color
        )

        draw.text(
            (x1 + 4, y1 - text_height + 3),
            text,
            font=font,
            fill=(0, 0, 0)
        )

        counts[label] = counts.get(label, 0) + 1

    return counts


# Main
def main():
    if HF_API_KEY == "your_huggingface_api_key_here":
        print("❌ Please add your Hugging Face API key first.")
        return

    path = ask_image()

    with open(path, "rb") as f:
        img_bytes = f.read()

    try:
        detections = detect_objects(path, img_bytes)
    except Exception as e:
        print("❌", e)
        return

    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    counts = annotate_image(img, detections)

    output = f"annotated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(output)

    print(f"\n✅ Saved output: {output}")

    if counts:
        print("\n🎉 Objects detected:")
        for label, count in sorted(
            counts.items(),
            key=lambda x: (-x[1], x[0])
        ):
            print(f"• {EMOJI.get(label.lower(), '✨')} {label}: {count}")
    else:
        print("🤔 No confident detections found.")

    print("\n⚠️ AI detections may not always be accurate.")


if __name__ == "__main__":
    main()