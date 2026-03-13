# 👓 Smart Glasses AI Assistant for Visually Impaired

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-red)
![Python](https://img.shields.io/badge/Python-3.11-blue) ![Computer
Vision](https://img.shields.io/badge/AI-Computer%20Vision-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

An **AI-powered Smart Glasses system** designed to assist visually
impaired individuals using **Raspberry Pi 4**, **Computer Vision**, and
**real‑time voice feedback**.

The system detects **objects, faces, emotions, and text**, then converts
them into **audio guidance** to help users understand their
surroundings.

------------------------------------------------------------------------

# 🚀 Key Features

### 🧍 Real-Time Object Detection

Detects objects around the user and announces them via voice.

Examples: - Person - Car - Bicycle - Chair - Door - Obstacles

Example voice output: \> "Person detected ahead."

------------------------------------------------------------------------

### 😀 Face Detection & Recognition

Recognizes known individuals and alerts the user.

Features: - Face enrollment system - Face database - Unknown person
detection

Example outputs:

> "Tharindu is in front of you."\
> "Unknown person detected."

------------------------------------------------------------------------

### 😊 Emotion Detection

Analyzes facial expressions.

Supported emotions: - Happy - Sad - Angry - Neutral - Surprise

Example:

> "Tharindu looks happy."

------------------------------------------------------------------------

### 📖 OCR Text Reading

Reads text from the environment.

Examples: - Signs - Books - Screens - Labels

Example output:

> "Text detected: Exit door."

------------------------------------------------------------------------

### 🔊 Intelligent Voice Feedback

Smart voice system with:

-   Audio priority queue
-   Cooldown timers
-   Message formatting
-   Event-based announcements

This prevents **repeated or unnecessary voice alerts**.

------------------------------------------------------------------------

# 🧠 AI Processing Workflow

    Camera
       │
       ▼
    Frame Buffer
       │
       ▼
    Object Detection
       │
       ├── Person detected
       │       ▼
       │   Face Detection
       │       ▼
       │   Face Recognition
       │       ▼
       │   Emotion Detection
       │
       ├── Text detected
       │       ▼
       │       OCR
       │
       ▼
    Context Fusion
       ▼
    Decision Engine
       ▼
    Speech Manager
       ▼
    Audio Queue
       ▼
    TTS Engine

------------------------------------------------------------------------

# 🏗 Project Architecture

    smart_glasses/
    │
    ├── main.py
    ├── config.py
    ├── requirements.txt
    │
    ├── boot/
    │   ├── smartglasses.service
    │   └── autostart_setup.sh
    │
    ├── core/
    │   ├── app_state.py
    │   ├── scheduler.py
    │   ├── event_bus.py
    │   ├── cooldown_manager.py
    │   └── mode_manager.py
    │
    ├── camera/
    │   ├── camera_stream.py
    │   ├── frame_buffer.py
    │   └── camera_utils.py
    │
    ├── pipelines/
    │   ├── object_pipeline.py
    │   ├── face_pipeline.py
    │   ├── emotion_pipeline.py
    │   ├── ocr_pipeline.py
    │   └── context_fusion.py
    │
    ├── audio/
    │   ├── tts_engine.py
    │   ├── audio_queue.py
    │   ├── speech_manager.py
    │   └── message_formatter.py
    │
    ├── models/
    ├── utils/
    ├── data/
    └── logs/

------------------------------------------------------------------------

# 💻 Hardware Requirements

-   🍓 Raspberry Pi 4
-   📷 Raspberry Pi Camera Module 2 (IMX219)
-   🔋 Portable battery pack
-   🎧 Earphones / speaker
-   💾 32GB+ MicroSD card

------------------------------------------------------------------------

# 🖥 Software Requirements

-   Raspberry Pi OS (Bookworm)
-   Python 3.11
-   OpenCV
-   ONNX Runtime
-   NumPy
-   TTS engine (pyttsx3 / PicoTTS)

------------------------------------------------------------------------

# ⚙️ Installation

Clone repository:

``` bash
git clone https://github.com/yourusername/smart-glasses-ai.git
cd smart-glasses-ai
```

Create virtual environment:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# ▶️ Running the System

``` bash
python main.py
```

The system will begin:

-   capturing camera frames
-   detecting objects
-   recognizing faces
-   reading text
-   speaking alerts

------------------------------------------------------------------------

# 👤 Face Enrollment

Add a new person:

``` bash
python training/enroll_faces.py --name "PersonName"
```

Then build the face database:

``` bash
python training/build_face_db.py
```

------------------------------------------------------------------------

# 🔄 Auto Start on Raspberry Pi

Enable automatic startup:

``` bash
sudo bash boot/autostart_setup.sh
```

This installs:

    smartglasses.service

------------------------------------------------------------------------

# ⚡ Performance Optimizations

This system uses:

-   Multi‑threaded architecture
-   Frame skipping strategy
-   Event‑driven model activation
-   ROI based processing
-   Priority speech queue

These optimizations allow **smooth real‑time AI on Raspberry Pi**.

------------------------------------------------------------------------

# 🔬 Research Purpose

This project is developed as a **research assistive technology system**
to improve mobility and independence for visually impaired individuals.

------------------------------------------------------------------------

# 🛣 Future Improvements

-   Sinhala voice feedback
-   Voice command control
-   Outdoor navigation assistance
-   Obstacle distance estimation
-   GPS navigation
-   Mobile companion app

------------------------------------------------------------------------

# 📜 License

© 2026 VisionGuide Research Team

------------------------------------------------------------------------

# ❤️ Acknowledgements

Special thanks to:

-   Raspberry Pi Foundation
-   OpenCV community
-   ONNX Runtime
-   Open source AI researchers

------------------------------------------------------------------------
