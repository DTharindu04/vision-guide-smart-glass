# 👓 VisionGuide -- AI Smart Glasses for Visually Impaired

<p align="center">

![Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry%20Pi%204-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Computer%20Vision-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</p>

------------------------------------------------------------------------

# 🌍 Project Overview

**VisionGuide** is an **AI-powered smart glasses system** designed to
assist **visually impaired individuals** by interpreting the surrounding
environment and converting visual information into **real-time voice
guidance**.

Using **Raspberry Pi, Computer Vision, and Artificial Intelligence**,
the system can:

-   👤 Recognize people
-   🚶 Detect obstacles
-   😊 Identify emotions
-   📖 Read text
-   🔊 Provide intelligent audio feedback

The goal is to **enhance independence and safety** for visually impaired
users.

------------------------------------------------------------------------

# ❗ Problem Statement

According to the **World Health Organization**, over **285 million
people worldwide** are visually impaired.

Visually impaired individuals face daily challenges such as:

-   Navigating unfamiliar environments
-   Avoiding obstacles
-   Recognizing people
-   Reading signs or text
-   Understanding social interactions

Existing assistive devices are often:

-   ❌ Expensive
-   ❌ Limited in functionality
-   ❌ Not portable
-   ❌ Not intelligent enough

Therefore, there is a strong need for a **low-cost intelligent wearable
system** that can help visually impaired people **perceive their
surroundings more effectively**.

------------------------------------------------------------------------

# 💡 Proposed Solution

This project introduces **VisionGuide Smart Glasses**, a **multi-AI
assistive system** that provides real-time environmental awareness.

The system uses **computer vision and speech feedback** to assist users
in understanding their surroundings.

The device can:

✔ Detect objects around the user\
✔ Recognize known individuals\
✔ Identify emotions\
✔ Read text from the environment\
✔ Provide voice alerts and guidance

All processing runs on a **Raspberry Pi 4 embedded system**.

------------------------------------------------------------------------

# 🧠 System Workflow

    Camera
       │
       ▼
    Frame Capture
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
    Voice Output

------------------------------------------------------------------------

# 🏗 System Architecture

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

# 🚀 Key Features

### 🧍 Real-Time Object Detection

Detects surrounding objects such as:

-   Person
-   Car
-   Bicycle
-   Chair
-   Door
-   Obstacles

Example voice output:

> 🔊 "Person detected ahead."

------------------------------------------------------------------------

### 👤 Face Detection & Recognition

The system recognizes **known individuals**.

Features:

-   Face enrollment
-   Face database
-   Unknown person detection

Example output:

> 🔊 "Tharindu is in front of you."

or

> 🔊 "Unknown person detected."

------------------------------------------------------------------------

### 😊 Emotion Detection

Detects facial emotions:

-   Happy
-   Sad
-   Angry
-   Neutral
-   Surprise

Example:

> 🔊 "Tharindu looks happy."

------------------------------------------------------------------------

### 📖 OCR Text Reading

Reads text from the environment.

Examples:

-   Signs
-   Books
-   Labels
-   Screens

Example output:

> 🔊 "Text detected: Exit door."

------------------------------------------------------------------------

### 🔊 Intelligent Voice Feedback

Advanced voice system includes:

-   Priority audio queue
-   Cooldown timers
-   Event-based speech
-   Smart message formatting

This prevents **repeated or unnecessary alerts**.

------------------------------------------------------------------------

# ⚙ Technology Stack

  Component         Technology
  ----------------- ------------------------------
  Hardware          Raspberry Pi 4
  Programming       Python 3.11
  Computer Vision   OpenCV
  AI Inference      ONNX Runtime
  OCR               Tesseract
  Voice Feedback    pyttsx3 / PicoTTS
  Camera            Raspberry Pi Camera Module 2

------------------------------------------------------------------------

# 💻 Hardware Requirements

-   🍓 Raspberry Pi 4
-   📷 Raspberry Pi Camera Module 2
-   🔋 Portable battery pack
-   🎧 Earphones or speaker
-   💾 MicroSD card (32GB+)

------------------------------------------------------------------------

# 🖥 Software Requirements

-   Raspberry Pi OS **Bookworm**
-   Python **3.11**
-   OpenCV
-   NumPy
-   ONNX Runtime

------------------------------------------------------------------------

# ⚙ Installation

Clone repository

``` bash
git clone https://github.com/yourusername/visionguide-smart-glasses.git
cd visionguide-smart-glasses
```

Create virtual environment

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# ▶ Running the System

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

Add a new person

``` bash
python training/enroll_faces.py --name "PersonName"
```

Then build the face database

``` bash
python training/build_face_db.py
```

------------------------------------------------------------------------

# 🔄 Auto Start on Raspberry Pi

``` bash
sudo bash boot/autostart_setup.sh
```

This installs

    smartglasses.service

so the system starts automatically when the Raspberry Pi boots.

------------------------------------------------------------------------

# ⚡ Performance Optimizations

To run efficiently on Raspberry Pi, the system includes:

-   Multi-threaded architecture
-   Frame skipping strategies
-   ROI-based processing
-   Event-driven model activation
-   Priority speech queue

These allow **smooth real-time AI processing on embedded hardware**.

------------------------------------------------------------------------

# 🔬 Research Impact

This project contributes to **assistive technology research** by
providing:

-   A **low-cost AI wearable system**
-   Real-time **environment awareness**
-   **Improved mobility for visually impaired individuals**

------------------------------------------------------------------------

# 🛣 Future Improvements

-   🇱🇰 Sinhala voice assistant
-   🎤 Voice commands
-   🧭 Navigation assistance
-   📍 GPS integration
-   📱 Mobile companion app
-   🧠 Edge AI optimization

------------------------------------------------------------------------

# 📜 License

© 2026 VisionGuide Research Team
<<<<<<< HEAD

Licensed under **MIT License**
=======
>>>>>>> 6b79c6e2a39b3c5911795717b59032200932cdd1

------------------------------------------------------------------------

# ❤️ Acknowledgements

-   Raspberry Pi Foundation
-   OpenCV Community
-   ONNX Runtime Developers
-   Open Source AI Research Community

------------------------------------------------------------------------
