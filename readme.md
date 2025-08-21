# 🌊 WaveBrush — Draw with Hand Gestures using OpenCV + MediaPipe ✋🖌️

**WaveBrush** is a **real-time AI-powered virtual painting system** built with **OpenCV** and **MediaPipe**.
It allows you to draw, erase, and switch colors on a digital canvas using **hand gestures only** — no mouse or touchscreen required.

It reuses a modular `HandTrackingModule.py` for precise hand landmark detection and finger gesture recognition to make drawing smooth and intuitive.

---

<!-- ## 📸 Demo

<p align="center">  
  <img src="" width="120"/>  
  <img src="" width="120"/>  
  <img src="" width="120"/>  
</p>   -->

---

## 📦 Project Structure

```
WaveBrush/
│
├── VirtualPainter.py          # Main app for gesture-based drawing
├── HandTrackingModule.py      # Custom hand tracking class using MediaPipe
├── PaintImage/                # Toolbar images (colors, eraser, etc.)
│   ├── color1.jpg
│   ├── color2.jpg
│   ├── color3.jpg
│   └── eraser.jpg
```

---

## 🧠 How It Works

1. Webcam captures live video feed.
2. `HandTrackingModule.py` detects hand landmarks using **MediaPipe Hands**.
3. Gestures are recognized:

   * ✌️ **Selection Mode** → Two fingers (index + middle) up → select color/eraser from the top toolbar.
   * ☝️ **Drawing Mode** → One finger (index only) up → draw lines on the canvas with the selected color.
4. Eraser works by drawing thick black lines over the canvas.
5. The drawing is preserved by combining a **transparent canvas** with the live video feed.

---

## 📌 Features

* ✅ Real-time gesture-based drawing
* ✅ Multiple brush colors
* ✅ Eraser tool support
* ✅ Customizable brush & eraser thickness
* ✅ Smooth drawing experience with live feed overlay

---

## 🔧 Requirements

* Python 3.x
* OpenCV
* Mediapipe
* NumPy

Install required libraries with:

```bash
pip install opencv-python mediapipe numpy
```

---

## 🚀 Getting Started

### 1. Clone or Download

```bash
git clone https://github.com/your-username/WaveBrush.git
cd WaveBrush
```

### 2. Place Toolbar Images

Add images for colors and eraser in a folder called `PaintImage/`.
For example: `color1.jpg`, `color2.jpg`, `color3.jpg`, `eraser.jpg`.

### 3. Run the App

```bash
python VirtualPainter.py
```

Press `q` to quit the application.

---

## 📊 Landmark Reference (MediaPipe IDs)

```
Thumb   : 4
Index   : 8
Middle  : 12
Ring    : 16
Pinky   : 20
```

---

## 🚫 Limitations

* ✋ Single-hand detection (no dual-hand support yet).
* 🎨 Limited toolbar options (currently only 3–4 colors + eraser).
* 💡 Requires good lighting for reliable tracking.

---

## 🧩 Future Improvements

* Add more brush styles (spray, shapes, thickness slider).
* Multi-hand support (collaborative drawing).
* Gesture shortcuts (clear canvas, undo/redo).
* Save drawings as images.

---

## 👤 Author

**Made with ❤️ by Vanshaj P Mohan, a Data Science Enthusiast.**

---

