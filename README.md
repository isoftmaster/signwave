# SignWave - Real-Time AI Sign Language Translator

**Developer:** Tanveer Alam

---

## Overview

SignWave is a real-time system that translates Sign Language into spoken language using computer vision and deep learning. 
It is designed to be completely local, offline, and free—bridging the communication gap between deaf individuals and hearing people in environments where interpreters are unavailable (clinics, schools, public services).

This project features a beautiful web dashboard that can be accessed remotely via a mobile device (QR code integration) to act as a live subtitle screen. It also features a two-way communication system using the Web Speech API.

---

## How It Works

- **Computer Vision:** Captures live video from a webcam and detects hands and upper-body landmarks using MediaPipe.
- **Deep Learning:** Encodes skeleton keypoints into mathematical sequences and classifies them in real-time using a custom PyTorch Bi-LSTM neural network.
- **Offline TTS:** Uses Windows Native SAPI (PowerShell) for zero-latency offline text-to-speech generation.
- **Web Dashboard:** Streams a live MJPEG feed and Server-Sent Events (SSE) to a premium glassmorphism dashboard built with Vanilla CSS and Flask.

---

## Core Features

- ⚡ **Real-time multi-landmark tracking** (hands + upper body)
- 🧠 **Temporal gesture recognition** using sequence PyTorch models
- 🎙️ **Zero-latency offline TTS** (Text-to-Speech)
- 📱 **Mobile Dashboard Companion:** Generate a QR code to view live subtitles on a phone
- 🎤 **Two-Way Communication:** Hearing people can use the microphone to transcribe text back to the deaf user
- 🔒 **100% Privacy:** Fully local execution. No cloud APIs, no subscriptions.

---

## Tech Stack

| Layer | Technologies |
|------|--------------|
| **Frontend UI** | HTML5, Vanilla CSS (Glassmorphism), JavaScript |
| **Backend & APIs** | Python, Flask, Server-Sent Events (SSE) |
| **Computer Vision** | OpenCV, MediaPipe Holistic |
| **Machine Learning** | PyTorch (Bi-LSTM) |
| **Voice / Speech** | Windows SAPI (PowerShell), Web Speech API |

---

## Installation & Usage

1. **Clone the repository** and navigate to the folder.
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the App:**
   ```bash
   python web_app.py
   ```
5. Open `http://localhost:5000` in your web browser. 
6. (Optional) Scan the QR code on the dashboard to open the interface on your mobile phone on the same Wi-Fi network.

---

## Adding Custom Signs

You can train the AI to learn your own unique gestures!

1. Open `label_map.json` and add your new word (e.g., `"7": "hello"`).
2. Open `src/config_voice.py` and map the word to spoken text in `GESTURE_TO_TEXT`.
3. Stop the web app, and run the recording script:
   ```bash
   python src/camera_record.py --gesture hello --reps 30
   ```
4. Retrain the model on the new data:
   ```bash
   python src/train.py
   ```

---
*Developed by Tanveer Alam*
