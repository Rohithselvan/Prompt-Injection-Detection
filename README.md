<img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/e7b072a8-5ae7-4d14-b5c2-c86778ff50cf" />

<h1 align="center">🛡️ Prompt Injection Detector</h1>
<p align="center">

<img src="https://img.shields.io/badge/Python-3.10-blue.svg"/>
<img src="https://img.shields.io/badge/FastAPI-Framework-green"/>
<img src="https://img.shields.io/badge/DistilBERT-HuggingFace-orange"/>
<img src="https://img.shields.io/badge/Google-Gemini-blue"/>
<img src="https://img.shields.io/badge/License-MIT-yellow"/>

</p>
<p align="center">
A multi-modal AI security system that detects prompt injection attacks before they reach a Large Language Model.
</p>

<p align="center">
Built with <b>FastAPI</b> • <b>DistilBERT</b> • <b>Google Gemini</b> • <b>Whisper</b> • <b>Tesseract OCR</b>
</p>

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Dataset](#-dataset)
- [Training the Model](#-training-the-model)
- [Model Loading](#-model-loading)
- [Running the API](#-running-the-api)
- [Demo](#-demo)
- [Results](#-results)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

# 🔍 Overview

Prompt Injection Detector is a **multi-modal AI security application** that protects Large Language Models from malicious prompts before they reach the AI model.

Instead of relying on a single classifier, the system combines a **rule-based heuristic engine** with a **fine-tuned DistilBERT model** to detect prompt injections, jailbreak attempts, role-play attacks, and social engineering prompts.

The application supports **text**, **images**, and **audio** as inputs. Images are processed using **Tesseract OCR**, audio is transcribed using **OpenAI Whisper**, and safe inputs are forwarded to **Google Gemini** for response generation.

---

# ✨ Features

- 🛡️ Two-layer prompt injection detection
- 🤖 Fine-tuned DistilBERT classifier
- 📝 Text input support
- 🖼️ OCR-based image analysis
- 🎙️ Audio transcription using Whisper
- ⚡ Fast heuristic filtering
- 💬 Google Gemini integration
- 📊 Confidence scores and timing metrics
- 📈 Session statistics
- 🎨 Modern responsive UI
- 🤗 Automatic dataset download
- ☁️ Automatic Hugging Face model loading

---

# ⚙️ How It Works

```text
                 User Input
          (Text / Image / Audio)
                     │
                     ▼
        ┌─────────────────────────┐
        │    Preprocessing        │
        │ OCR • Whisper • Cleanup │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │ Layer 1                 │
        │ Heuristic Detection     │
        └────────────┬────────────┘
                     │
             Unsafe? │
          Yes ───────┘
                     ▼
                🚨 Blocked

                     │ No
                     ▼
        ┌─────────────────────────┐
        │ Layer 2                 │
        │ DistilBERT Classifier   │
        └────────────┬────────────┘
                     │
             Unsafe? │
          Yes ───────┘
                     ▼
                🚨 Blocked

                     │ No
                     ▼
          Google Gemini Response

                     ▼
            Safe Response Returned
```

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Machine Learning | PyTorch, Hugging Face Transformers |
| NLP | DistilBERT |
| OCR | Tesseract OCR |
| Speech Recognition | OpenAI Whisper |
| LLM | Google Gemini 2.5 Flash |
| Dataset | Hugging Face Datasets |

---

# 📁 Project Structure

```text
Prompt_Injection_Detection/
│
├── core/
│   ├── asr.py
│   ├── config.py
│   ├── ocr.py
│   └── preprocess.py
│
├── pipeline/
│   ├── classifier.py
│   ├── gemini.py
│   └── heuristic.py
│
├── training/
│   ├── dataset.py
│   ├── downloader.py
│   └── trainer.py
│
├── model/
│
├── static/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── main.py
├── train.py
├── requirements.txt
├── .env.example
└── README.md
```

> **Note**
>
> The `model/` directory is populated automatically either by training a new model or by downloading the pre-trained model from Hugging Face during the first run.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Prompt_Injection_Detection.git

cd Prompt_Injection_Detection
```

Create a virtual environment

### Windows

```bash
python -m venv .venv

.\.venv\Scripts\Activate
```

### Linux / macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Create a `.env` file using `.env.example`

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Get your free Gemini API key from:

https://aistudio.google.com/app/apikey

---

# 📊 Dataset

The training dataset is hosted on Hugging Face and is automatically downloaded when required.

**Dataset Repository**

https://huggingface.co/datasets/Rohith1872/prompt-injection-dataset

Simply run:

```bash
python train.py
```

If the dataset is missing, it will be downloaded automatically before training begins.

---

# 🏋️ Training the Model

Train the DistilBERT classifier using:

```bash
python train.py
```

The training pipeline automatically:

- 📥 Downloads the dataset (if missing)
- 🤖 Fine-tunes DistilBERT
- 💾 Saves the trained model and tokenizer
- 📂 Stores all generated files inside the `model/` directory

Generated files include:

```text
model/
├── config.json
├── model.safetensors
├── tokenizer.json
├── tokenizer_config.json
├── special_tokens_map.json
└── vocab.txt
```

---

# 🤖 Model Loading

The project supports **two ways** to use the classifier.

## 🚀 Option 1 — Use the Pre-trained Model (Recommended)

When the application starts, it first checks whether a trained model already exists inside the `model/` directory.

If no model is found, it automatically:

- 🔍 Checks for local model files
- ⬇️ Downloads the latest trained model from Hugging Face
- 💾 Saves it locally
- ⚡ Uses the downloaded model for all future runs

**Model Repository**

https://huggingface.co/Rohith1872/DistilBERT_Classifier

---

## 🏋️ Option 2 — Train Your Own Model

If you prefer to build your own classifier:

```bash
python train.py
```

Once training is complete, the generated model inside the `model/` directory is automatically used by the application instead of downloading from Hugging Face.

---

## 🔄 Model Loading Workflow

```text
Application Starts
        │
        ▼
Local model exists?
        │
   ┌────┴────┐
   │         │
  Yes        No
   │          │
   │      Download
   │      from HF
   │          │
   │      Save locally
   └──────┬───┘
          ▼
     Load DistilBERT
          │
          ▼
 Ready for Inference
```

---

# ▶️ Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser:

| URL | Description |
|------|-------------|
| http://localhost:8000 | Web Interface |
| http://localhost:8000/docs | Swagger API |
| http://localhost:8000/redoc | ReDoc Documentation |

---

# 📸 Demo

### 📝 Text Input

<img width="551" height="447" alt="Imaage" src="https://github.com/user-attachments/assets/e55aa8a4-864e-4723-acb5-7e5b4455b7ba" />

---

### 🖼️ Image OCR Detection

<img width="1445" height="447" alt="Image" src="https://github.com/user-attachments/assets/a89b3d2c-331a-47c3-a40e-bce3d9a2d52b" />

---

### 🎙️ Audio Detection

<img width="1132" height="353" alt="Image" src="https://github.com/user-attachments/assets/d86395bc-71ae-4131-a79f-ebe8e7bf83b2" />

---

### 🚨 Unsafe Prompt Detection

<img width="1140" height="352" alt="Image" src="https://github.com/user-attachments/assets/2e278aa1-6893-4e48-ba45-f58d9f72efea" />

---

### ✅ Safe Prompt Response

<img width="1278" height="395" alt="Image" src="https://github.com/user-attachments/assets/e6acd2e4-e909-4d93-a1e7-a1851cdf8085" />

---

# 📈 Example Pipeline

```
Text / Image / Audio
        │
        ▼
 OCR / Whisper Processing
        │
        ▼
 Heuristic Detection
        │
        ▼
 DistilBERT Classification
        │
        ▼
 Safe?
   │
 ┌─┴───────────────┐
 │                 │
No                 Yes
 │                  │
 ▼                  ▼
Blocked      Google Gemini
                    │
                    ▼
             Safe AI Response
```

---

# 📊 Results

The proposed two-layer security pipeline successfully detects a wide range of prompt injection attacks while allowing legitimate requests to reach the language model.

### Key Outcomes

- ✅ Two-stage detection using **Heuristic Filtering** and **DistilBERT Classification**
- 📝 Supports **Text**, **Image (OCR)**, and **Audio (Whisper)** inputs
- 🚨 Blocks prompt injections, jailbreaks, role-play attacks, and malicious prompts before they reach the LLM
- 🤖 Automatically forwards verified safe inputs to **Google Gemini** for response generation
- ⚡ Fast inference with real-time confidence scores and processing metrics
- 🤗 Automatic dataset and model download from **Hugging Face**
- 💾 Supports both **local model loading** and **automatic model retrieval** for easy deployment
- 🎨 Interactive web interface with live threat analysis and session statistics

---

### Highlights

| Capability | Status |
|------------|:------:|
| Text Detection | ✅ |
| Image OCR Detection | ✅ |
| Audio Detection | ✅ |
| Heuristic Filtering | ✅ |
| DistilBERT Classification | ✅ |
| Gemini Integration | ✅ |
| Automatic Dataset Download | ✅ |
| Automatic Model Download | ✅ |
| Responsive Web Interface | ✅ |

# 🚀 Future Improvements

- 🔐 Multi-language prompt injection detection
- 📱 Mobile application
- 🌐 Browser extension support
- ☁️ Cloud deployment
- 📊 Detection analytics dashboard
- ⚡ Quantized models for faster inference
- 🧠 Support for additional LLMs

---

# 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

### 🛡️ Prompt Injection Detector

**FastAPI • DistilBERT • Gemini • Whisper • Tesseract OCR**

⭐ If you found this project helpful, consider giving it a star!

</div>
