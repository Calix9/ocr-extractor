from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os, uuid, base64, io
from pathlib import Path
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\TBS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED = {".jpg", ".jpeg", ".png"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def preprocess_image(pil_img):
    img = np.array(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if len(img.shape) == 3 else img
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    return Image.fromarray(cv2.filter2D(thresh, -1, kernel))


def run_ocr(pil_img):
    enhanced = preprocess_image(pil_img)
    raw_text = pytesseract.image_to_string(pil_img, config="--psm 6")
    enh_text = pytesseract.image_to_string(enhanced, config="--psm 6")
    best_text = enh_text if len(enh_text.split()) >= len(raw_text.split()) else raw_text

    data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
    words, confs = [], []
    for i, word in enumerate(data["text"]):
        word = word.strip()
        conf = int(data["conf"][i])
        if word and conf > 0:
            words.append({"text": word, "x": data["left"][i], "y": data["top"][i],
                          "w": data["width"][i], "h": data["height"][i], "conf": conf})
            confs.append(conf)

    return {
        "text": best_text.strip(),
        "words": words,
        "word_count": len(best_text.split()),
        "char_count": len(best_text.strip()),
        "confidence": round(sum(confs)/len(confs), 1) if confs else 0,
        "img_width": pil_img.width,
        "img_height": pil_img.height,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["image"]
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED:
        return jsonify({"error": "Use JPG or PNG."}), 400

    filename = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        pil_img = Image.open(save_path).convert("RGB")
        result = run_ocr(pil_img)
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=92)
        result["image_b64"] = base64.b64encode(buf.getvalue()).decode("utf-8")
        result["filename"] = file.filename
        result["size_kb"] = round(os.path.getsize(save_path) / 1024, 1)
        result["timestamp"] = datetime.now().strftime("%d %b %Y, %H:%M")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)


@app.route("/ocr-region", methods=["POST"])
def ocr_region():
    data = request.get_json()
    b64 = data.get("image_b64")
    x, y, w, h = int(data.get("x",0)), int(data.get("y",0)), int(data.get("w",0)), int(data.get("h",0))
    if not b64 or w <= 0 or h <= 0:
        return jsonify({"error": "Invalid region"}), 400

    try:
        pil_img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
        iw, ih = pil_img.size
        x, y = max(0, min(x, iw)), max(0, min(y, ih))
        cropped = pil_img.crop((x, y, min(x+w, iw), min(y+h, ih)))
        cw, ch = cropped.size
        if cw < 200 or ch < 50:
            scale = max(200/cw, 50/ch, 2.0)
            cropped = cropped.resize((int(cw*scale), int(ch*scale)), Image.LANCZOS)
        result = run_ocr(cropped)
        return jsonify({"text": result["text"], "word_count": result["word_count"], "confidence": result["confidence"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)