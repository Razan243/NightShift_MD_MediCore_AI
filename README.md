# 🩺 NightShift MD — MediCore AI

> An AI-powered clinical decision-support prototype for analyzing medical reports and generating structured emergency triage insights.

## 📌 Overview

**NightShift MD / MediCore AI** is a multi-agent AI project designed to process medical reports and transform unstructured clinical information into a structured assessment.

The system analyzes an uploaded PDF medical report through a sequence of specialized agents that extract patient information, medical records, patient history, and emergency triage findings.

The project was developed as a practical implementation of a **Multi-Agent AI workflow** using Python, LangGraph, FastAPI, and a local language model.

---

## 🎯 Project Objective

The main objective of NightShift MD is to demonstrate how AI agents can assist in organizing and analyzing clinical information.

The system follows this workflow:

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

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- LangGraph
- PyPDF2
- Transformers
- google/flan-t5-small

### Frontend

- HTML5
- CSS3
- JavaScript
- PDF.js

### AI & Workflow

- Multi-Agent AI architecture
- LangGraph workflow orchestration
- Local language model inference
- Rule-based clinical information extraction
- Structured final report generation

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

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Razan243/NightShift_MD_MediCore_AI.git
cd NightShift_MD_MediCore_AI

### 2. Create a virtual environment

```bash
python -m venv .venv
### 3. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate

pip install -r backend/requirements.txt

uvicorn backend.main:app --reload
http://127.0.0.1:8000
