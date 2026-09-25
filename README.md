# 🩺 NightShift MD — MediCore AI

> An AI-powered clinical decision-support prototype for analyzing medical reports and generating structured emergency triage insights.

---

## 📌 Overview

**NightShift MD / MediCore AI** is a Multi-Agent AI project designed to process medical reports and transform unstructured clinical information into a structured clinical assessment.

The system accepts a medical report in PDF format and processes it through a sequence of specialized agents that extract patient information, medical records, patient history, emergency findings, and a clinical summary.

The project demonstrates the practical application of **Artificial Intelligence, Multi-Agent Systems, Natural Language Processing, and workflow orchestration** in a clinical decision-support scenario.

---

## ✨ Features

- 📄 Medical PDF report processing
- 👤 Patient information extraction
- 📋 Medical records extraction
- 🕒 Patient history and timeline organization
- 🚨 Emergency triage assessment
- 🔎 Critical clinical findings detection
- 🧠 AI-generated clinical summary
- 📊 Structured final clinical report
- ✅ Final report validation
- 🌐 Web-based interface
- 🤖 Multi-Agent workflow architecture

---

## 🎯 Project Objective

The main objective of NightShift MD is to demonstrate how AI agents can assist in organizing and analyzing clinical information from medical reports.

The system follows a sequential workflow:

```text
Medical PDF
     ↓
Patient Data Agent
     ↓
Medical Records Agent
     ↓
History Agent
     ↓
Triage Agent
     ↓
Summary Agent
     ↓
Final Clinical Report
```

---

## 🤖 Multi-Agent Workflow

### 1. Patient Data Agent

Extracts essential patient information from the medical report, including:

- Age
- Gender
- Symptoms
- Vital signs
- Clinical conditions
- Other relevant information

### 2. Medical Records Agent

Identifies relevant medical records such as:

- Previous medical status
- Medications
- Tests and examinations
- Emergency interventions
- Pathological findings

### 3. History Agent

Organizes the patient's medical history into:

- Long-term care
- Previous status
- Recent history
- Timeline events

### 4. Triage Agent

Analyzes critical clinical findings and determines the emergency priority based on the extracted information.

The current prototype identifies critical findings such as:

- Cardiac arrest
- Unresponsiveness
- No distal pulses
- Heart rate of 0
- Respiratory rate of 0

### 5. Summary Agent

Generates a structured clinical summary based on:

- Patient information
- Symptoms
- Clinical history
- Acute findings
- Triage priority

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │     Medical PDF      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Patient Data Agent   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Medical Records      │
                         │ Agent                │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ History Agent        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Triage Agent         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Summary Agent        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Final Clinical       │
                         │ Report               │
                         └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- LangGraph
- PyPDF2
- Hugging Face Transformers
- `google/flan-t5-small`

### Frontend

- HTML5
- CSS3
- JavaScript
- PDF.js

### AI & Workflow

- Multi-Agent AI Architecture
- LangGraph Workflow Orchestration
- Local Language Model
- Natural Language Processing
- Rule-Based Clinical Information Extraction
- Structured Report Generation

---

## 📂 Project Structure

```text
NightShift_MD_MediCore_AI/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Razan243/NightShift_MD_MediCore_AI.git
cd NightShift_MD_MediCore_AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Run the Backend

```bash
uvicorn backend.main:app --reload
```

The FastAPI backend will be available at:

```text
http://127.0.0.1:8000
```

### 6. Open the Frontend

Open:

```text
frontend/index.html
```

The application allows the user to upload a medical PDF and generate a structured clinical assessment.

---

## 🌐 Live Demo

### Hugging Face Space

https://huggingface.co/spaces/razangewaily/NightShift_MD_MediCore_AI

### Live Application

https://razangewaily-nightshift-md-medicore-ai.static.hf.space

---

## 📄 Input

The system accepts medical reports in **PDF format**.

After uploading a report, the application extracts and organizes relevant information into structured sections.

---

## 📊 Generated Assessment

The generated assessment contains:

### Patient Data

- Age
- Gender
- Symptoms
- Vital signs
- Clinical conditions
- Relevant information

### Medical Records

- Previous medical status
- Medications
- Tests and examinations
- Emergency interventions
- Pathological findings

### Patient History

- Long-term care
- Previous status
- Recent history
- Clinical timeline

### Triage

- Emergency priority
- Critical findings
- Clinical reasoning
- Safety note

### Clinical Summary

A structured summary of the patient's condition and identified acute findings.

---

## 🔍 Final Report Validation

The system validates the final report to ensure that the required sections are present.

Required sections include:

- Patient Data
- Medical Records
- History
- Triage
- Clinical Summary

The final report also stores the name of the original source document.

---

## 🧠 Example Workflow

A medical PDF is uploaded to the application.

The system then:

```text
1. Extracts the PDF content
            ↓
2. Identifies patient information
            ↓
3. Extracts medical records
            ↓
4. Organizes the patient's history
            ↓
5. Identifies critical emergency findings
            ↓
6. Determines the triage priority
            ↓
7. Generates a structured clinical summary
            ↓
8. Produces the final clinical report
```

---

## ⚠️ Safety Notice

**NightShift MD / MediCore AI is a decision-support prototype and is not a medical diagnosis or treatment recommendation system.**

The project is intended for educational and demonstration purposes and should not replace professional medical judgment.

---

## 🎓 Project Context

This project demonstrates practical applications of:

- Artificial Intelligence
- Multi-Agent Systems
- Natural Language Processing
- Large Language Models
- Clinical Information Extraction
- Workflow Orchestration
- AI-Assisted Decision Support

---

## 👩‍💻 Author

**Razan Gewaily**

Computer Science Student — Artificial Intelligence

GitHub:

https://github.com/Razan243

---

## ⭐ Project

If you find this project useful or interesting, feel free to explore the repository and the implementation.
