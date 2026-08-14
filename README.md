# RoadGuard-AI : 
AI-powered road damage detection system using YOLO and Flask to identify road cracks, potholes, assess severity, prioritize repairs, and generate inspection reports.
# 🚧 RoadGuard AI
https://roadguard-ai-w98g.onrender.com/

### AI-Powered Road Damage Detection and Inspection System

RoadGuard AI is an AI-powered road inspection system designed to automatically detect and analyze road surface damages from images.

The system uses a trained YOLO object detection model to identify different types of road damage and provides confidence scores, severity levels, repair priorities, and recommended maintenance actions.

---

## 🌐 Project Website

> 🚧 Live deployment is currently not available.

The project is currently running locally using Flask.

A live website link will be added after deployment.

---

## 📌 Project Overview

Road damage such as cracks and potholes can create serious safety risks for road users and can become more expensive to repair when detection is delayed.

Traditional road inspection methods often require manual inspection, which can be time-consuming and difficult to scale.

RoadGuard AI provides an automated computer vision-based solution where users can upload a road image and the trained YOLO model analyzes the image to identify visible road damage.

The system then generates an inspection result containing:

- Detected damage type
- AI confidence score
- Damage severity
- Repair priority
- Recommended maintenance action
- AI detection visualization
- Inspection history

---

## 🎯 Objectives

The main objectives of RoadGuard AI are:

- To automate road damage detection using Artificial Intelligence.
- To identify cracks and potholes from road images.
- To reduce dependency on manual road inspection.
- To provide confidence scores for detected damages.
- To classify damage based on severity.
- To assign maintenance priorities.
- To provide recommended actions for detected damages.
- To maintain a history of road inspection reports.

---

## 🤖 AI Model

RoadGuard AI uses a **YOLO (You Only Look Once)** object detection model trained to identify road surface damage.

### Detection Classes

The current model supports 8 road damage classes:

1. Longitudinal Crack
2. Longitudinal Crack Wide
3. Transverse Crack
4. Transverse Crack Wide
5. Alligator Crack
6. Alligator Crack Sunken
7. Pothole
8. Pothole Deep

---

## 🔍 How It Works

```text
        Road Image
             │
             ▼
      Image Upload
             │
             ▼
       Flask Backend
             │
             ▼
       YOLO AI Model
             │
             ▼
     Damage Detection
             │
             ▼
   ┌──────────────────────┐
   │ Damage Type          │
   │ Confidence Score     │
   │ Severity              │
   │ Priority              │
   │ Recommendation        │
   └──────────────────────┘
             │
             ▼
      Inspection Report
      📁 Project Structure
RoadGuard-AI/
│
├── app.py
│
├── reports.json
│
├── requirements.txt
│
├── README.md
│
├── templates/
│   ├── index.html
│   ├── detect.html
│   └── reports.html
│
├── static/
│   └── uploads/
│
└── runs/
    └── detect/
        └── train-2/
            └── weights/
                └── best.pt

                project local host URL :https://roadguard-ai-w98g.onrender.com/
