# NightShift MD / MediCore AI

A frontend + FastAPI version of the Emergency Triage Multi-Agent AI project from `Final.ipynb`.

## Project flow

PDF upload → Patient Data Agent → Medical Records Agent → History Agent → Triage Agent → Summary Agent → Final Report

## Stack

- Frontend: HTML/CSS/JavaScript
- Backend: FastAPI
- PDF extraction: PyPDF2
- Local LLM: `google/flan-t5-small`
- Orchestration: LangGraph

## Run on Windows

1. Open a terminal in this folder.
2. Create/activate a virtual environment:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

3. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

4. Start the application:

```bash
uvicorn backend.main:app --reload
```

5. Open `http://127.0.0.1:8000`.

The first run downloads the FLAN-T5-small model from Hugging Face. CPU inference can take some time.

> This is a decision-support prototype, not a medical diagnosis or treatment system.
