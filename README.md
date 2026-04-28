# 🔍 OCR Image Text Extractor

> A professional web-based OCR tool built with **Flask** + **Tesseract** that lets you upload images, zoom in, draw a selection box over any region, and extract text instantly — right in your browser.

**Built by [Kelvin Mathew Mambosasa](https://github.com/calix9) · Tanzania 🇹🇿**

---

## ✨ Features

- 📤 **Drag & drop** image upload (JPG, PNG)
- 🔎 **Zoom in/out** with mouse scroll or toolbar buttons
- ✂️ **Region selection** — draw a box on any area to OCR just that part
- 🧠 **Full-image OCR** with word-level bounding box overlay
- 📊 **Confidence score**, word count, and character count display
- 📋 **One-click copy** for both full text and region text
- 🖐 **Pan mode** to navigate when zoomed in
- 🌑 **Dark UI** — clean, fast, professional

---

## 🖥️ Demo Preview

```
Upload Image → Zoom & Pan → Draw Selection → Get Text Instantly
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| OCR Engine | Tesseract 5.x + pytesseract |
| Image Processing | OpenCV, Pillow |
| Frontend | Vanilla HTML/CSS/JS (Canvas API) |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **Tesseract OCR Engine** — [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- **Git** — [Download](https://git-scm.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/calix9/ocr-extractor.git
cd ocr-extractor
```

---

### 2. Create a Virtual Environment

> ⚠️ **Always use a virtual environment.** This keeps project dependencies isolated from your system Python and prevents version conflicts.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt — this means the virtual environment is active.

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Tesseract OCR Engine

Tesseract is the OCR engine that powers text extraction. **Python alone cannot do OCR — Tesseract must be installed separately.**

**Windows:**

1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the `.exe` and follow the setup wizard
3. Note the install path (default is usually `C:\Users\<YourName>\AppData\Local\Programs\Tesseract-OCR\`)

Then open `app.py` and update this line to match your actual install path:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\YourName\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
```

**Ubuntu / Debian:**
```bash
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

Verify Tesseract is working:
```bash
tesseract --version
```

---

### 5. Run the App

```bash
python app.py
```

Open your browser and go to:
```
http://localhost:5000
```

---

## 📁 Project Structure

```
ocr-extractor/
├── app.py                  # Flask backend & OCR logic
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Frontend UI (Canvas + JS)
├── static/
│   └── uploads/            # Temporary image storage (auto-created)
└── README.md
```

---

## 📦 requirements.txt

```
flask
pytesseract
Pillow
opencv-python
numpy
```

Generate your own with:
```bash
pip freeze > requirements.txt
```

---

## 🎮 How to Use

| Action | How |
|--------|-----|
| Upload image | Drag & drop or click the upload area |
| Zoom in/out | Scroll with mouse wheel OR use toolbar buttons |
| Pan around | Click **Pan** mode then drag the image |
| Select a region | In **Select** mode, click and drag a box |
| OCR a region | The selected region is sent to the server automatically |
| Copy text | Click **copy** next to any text panel |
| Toggle word boxes | Click the **Words** button in the toolbar |
| Load new image | Click **New** in the toolbar |

---

## 🐛 Known Issues & Current Limitations

> These are active problems being worked on. Contributions and ideas are very welcome!

### 1. 🔤 Low Accuracy on Handwritten Text
Tesseract is trained primarily on printed/typed fonts. Handwritten notes or stylized text often produce poor results. Investigating integration with **Google Vision API** or **EasyOCR** as alternatives for handwriting.

### 2. 🔡 Special Characters & Symbols Get Garbled
Mathematical symbols, currency signs (e.g., `$`, `€`, `£`), and special Unicode characters are sometimes misread or dropped entirely. This is a known Tesseract limitation with its default English language model.

### 3. 🌍 Limited Multi-language Support
Currently only configured for English (`eng`). Documents in Swahili, Arabic, Chinese, or other languages will not extract correctly. Tesseract supports many languages via additional language packs but this is not yet wired into the UI.

### 4. 📐 Skewed or Rotated Images Reduce Accuracy
If the source image is not perfectly horizontal (e.g., a photo taken at an angle), the OCR accuracy drops significantly. Auto-deskew / rotation correction is not yet implemented.

### 5. 🖼️ Low-Resolution Images Produce Poor Results
Images below ~150 DPI tend to give poor extractions. The preprocessing pipeline (grayscale → denoise → threshold → sharpen) helps but cannot fully compensate for very blurry or pixelated inputs.

### 6. 📄 No PDF Support Yet
Currently only JPG and PNG are supported. PDF upload with per-page OCR is planned.

### 7. 🪟 Tesseract Path is Hardcoded for Windows
The Tesseract binary path is currently hardcoded in `app.py`. This means users on different machines or OS must manually update the path. A proper config file or auto-detection is planned.

---

## 🤝 Contributing

All contributions are welcome — bug fixes, new features, UI improvements, or even just ideas!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request and describe what you've changed

Please open an **Issue** first for major changes so we can discuss the approach together.

---

## 💡 Ideas for Future Features

- [ ] Multi-language OCR via Tesseract language packs
- [ ] Auto-deskew / image rotation correction
- [ ] PDF upload with page-by-page OCR
- [ ] Export extracted text to `.txt` or `.docx`
- [ ] History of past scans (localStorage or SQLite)
- [ ] Drag-to-reorder OCR regions
- [ ] Mobile-responsive touch support for region selection
- [ ] Integration with Google Vision API for higher accuracy

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Kelvin Mathew Mambosasa**
GitHub: [@calix9](https://github.com/calix9)
Location: Dar es Salaam, Tanzania 🇹🇿

---

> *"Always building. Always learning."*
