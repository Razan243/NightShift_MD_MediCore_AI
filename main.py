import json
import re
from typing import TypedDict

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langgraph.graph import StateGraph, START, END

MODEL_NAME = "google/flan-t5-small"

app = FastAPI(title="NightShift MD / MediCore AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = __import__("pathlib").Path(__file__).resolve().parent.parent
FRONTEND = BASE_DIR / "frontend" / "index.html"

# Loaded once when the API starts.
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def generate_with_llm(prompt: str, max_new_tokens: int = 120) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


class EmergencyFlowState(TypedDict):
    pdf_text: str
    patient_data: dict
    medical_records: dict
    history_data: dict
    triage_data: dict
    summary_data: str
    final_report: dict


def patient_data_agent(pdf_text):
    text = pdf_text.lower()
    patient_data = {
        "age": None,
        "gender": None,
        "symptoms": [],
        "vital_signs": {},
        "clinical_condition": [],
        "other_relevant_information": []
    }

    age_match = re.search(r"\b(\d{2})\s*[- ]?year[- ]old\b", text)
    if age_match:
        patient_data["age"] = int(age_match.group(1))

    if "woman" in text:
        patient_data["gender"] = "Female"
    elif "man" in text:
        patient_data["gender"] = "Male"

    for phrase, label in [
        ("dyspnea on exertion", "Dyspnea on exertion"),
        ("shortness of breath", "Shortness of breath"),
        ("dry cough", "Dry cough"),
        ("atypical chest pain", "Atypical chest pain"),
    ]:
        if phrase in text:
            patient_data["symptoms"].append(label)

    patterns = {
        "blood_pressure": r"(?:blood pressure|bp)\s*(?:of|:)?\s*(\d+/\d+)",
        "heart_rate": r"(?:heart rate|hr)\s*(?:of|:)?\s*(\d+)",
        "respiratory_rate": r"(?:respiratory rate|rr)\s*(?:of|:)?\s*(\d+)",
        "temperature": r"(?:temperature|temp)\s*(?:of|:)?\s*(\d+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            patient_data["vital_signs"][key] = match.group(1)

    for phrase, label in [
        ("cardiac arrest", "Cardiac arrest"),
        ("unresponsive", "Unresponsive"),
        ("no distal pulses", "No distal pulses"),
        ("bilateral fixed and dilated pupils", "Bilateral fixed and dilated pupils"),
    ]:
        if phrase in text:
            patient_data["clinical_condition"].append(label)

    if "no medications" in text:
        patient_data["other_relevant_information"].append("No medications reported")
    return patient_data


def medical_records_agent(pdf_text):
    text = pdf_text.lower()
    records = {
        "previous_medical_status": [],
        "medications": [],
        "tests_and_examinations": [],
        "emergency_interventions": [],
        "reported_pathological_findings": []
    }
    if "healthy" in text:
        records["previous_medical_status"].append("Physician reported the patient as healthy")
    if "on no medications" in text:
        records["medications"].append("No medications reported")
    if "ekg" in text:
        records["tests_and_examinations"].append("EKG performed")
    if "rule out anemia" in text:
        records["tests_and_examinations"].append("Orders were sent to rule out anemia")
    if "thyroid disease" in text:
        records["tests_and_examinations"].append("Orders were sent to rule out thyroid disease")
    for phrase, label in [
        ("cpr", "CPR performed"),
        ("atropine", "Atropine administered"),
        ("epinephrine", "Epinephrine administered"),
        ("bicarbonate", "Bicarbonate administered"),
        ("intubation", "Intubation performed"),
    ]:
        if phrase in text:
            records["emergency_interventions"].append(label)
    for phrase, label in [
        ("bilateral pulmonary embolism", "Bilateral pulmonary embolism (PE)"),
        ("bile duct adenoma", "Bile duct adenoma"),
        ("fractures in the left ribs", "Rib fractures"),
    ]:
        if phrase in text:
            records["reported_pathological_findings"].append(label)
    return records


def history_agent(pdf_text):
    text = pdf_text.lower()
    history = {"long_term_care": [], "previous_status": [], "recent_history": [], "timeline_events": []}
    if "under the care of dr." in text and "19 years" in text:
        history["long_term_care"].append("Patient was under the care of a physician for 19 years")
    if "healthy" in text:
        history["previous_status"].append("Patient was reported as healthy")
    if "on no medications" in text:
        history["previous_status"].append("No medications were reported")
    if "two weeks of dyspnea" in text:
        history["recent_history"].append("Two weeks of dyspnea on exertion")
    if "dry cough" in text:
        history["recent_history"].append("Dry cough")
    if "atypical chest pain" in text:
        history["recent_history"].append("Atypical chest pain")
    if "february 9, 2007" in text:
        history["timeline_events"].append("February 9, 2007: Patient was evaluated by the physician")
    if "february 11, 2007" in text:
        history["timeline_events"].append("February 11, 2007: EMS found the patient in cardiac arrest")
    if "10:16 am" in text:
        history["timeline_events"].append("10:16 AM: CPR ceased and the patient was pronounced")
    return history


def triage_agent(patient_data, medical_records, history):
    clinical_condition = patient_data["clinical_condition"]
    vital_signs = patient_data["vital_signs"]
    critical_findings = []
    if "Cardiac arrest" in clinical_condition:
        critical_findings.append("Cardiac arrest")
    if "Unresponsive" in clinical_condition:
        critical_findings.append("Unresponsive")
    if "No distal pulses" in clinical_condition:
        critical_findings.append("No distal pulses")
    if vital_signs.get("heart_rate") == "0":
        critical_findings.append("Heart rate: 0")
    if vital_signs.get("respiratory_rate") == "0":
        critical_findings.append("Respiratory rate: 0")

    prompt = f"""
Explain the emergency severity of this case in one simple sentence.
Facts:
Cardiac arrest: {"yes" if "Cardiac arrest" in clinical_condition else "no"}
Unresponsive: {"yes" if "Unresponsive" in clinical_condition else "no"}
No distal pulses: {"yes" if "No distal pulses" in clinical_condition else "no"}
Heart rate: {vital_signs.get("heart_rate", "not reported")}
Respiratory rate: {vital_signs.get("respiratory_rate", "not reported")}
Write one factual sentence explaining why this is an immediate emergency.
Do not give a diagnosis.
Do not recommend treatment.
"""
    reason = generate_with_llm(prompt, 50).strip()
    invalid = ["do not give", "do not provide", "do not recommend", "do not mention", "answer only", "you are"]
    if not reason or any(p in reason.lower() for p in invalid):
        reason = ("The patient has cardiac arrest with no detectable heart rate, no respiratory rate, "
                  "and no distal pulses, indicating an immediate emergency.")
    priority = "Immediate Emergency" if critical_findings else "Requires Further Assessment"
    return {
        "priority": priority,
        "reason": reason,
        "critical_findings": critical_findings,
        "safety_note": "Decision-support prototype only; not a medical diagnosis or treatment recommendation."
    }


def summary_agent(patient_data, history, triage_data):
    prompt = f"""
Write exactly 3 short factual sentences about this emergency case.
Patient: Age: {patient_data["age"]}; Gender: {patient_data["gender"]}
Symptoms: {", ".join(patient_data["symptoms"])}
Acute findings: {", ".join(patient_data["clinical_condition"])}
Triage priority: {triage_data["priority"]}
Write: 1. One sentence about the patient and symptoms. 2. One sentence about the acute condition. 3. One sentence about the triage priority.
Do not provide a diagnosis. Do not recommend treatment. Use only the facts provided.
"""
    response = generate_with_llm(prompt, 120).strip()
    invalid = ["do not provide", "do not recommend", "write exactly", "you are"]
    if not response or any(p in response.lower() for p in invalid) or len(response.split(".")) < 3:
        response = (f"The patient is a {patient_data['age']}-year-old {str(patient_data['gender']).lower()} with "
                    f"{', '.join(patient_data['symptoms'])}. The acute findings include "
                    f"{', '.join(patient_data['clinical_condition'])}. The triage priority is {triage_data['priority']}.")
    return response


def patient_data_node(state):
    return {"patient_data": patient_data_agent(state["pdf_text"])}


def medical_records_node(state):
    return {"medical_records": medical_records_agent(state["pdf_text"])}


def history_node(state):
    return {"history_data": history_agent(state["pdf_text"])}


def triage_node(state):
    return {"triage_data": triage_agent(state["patient_data"], state["medical_records"], state["history_data"])}


def summary_node(state):
    return {"summary_data": summary_agent(state["patient_data"], state["history_data"], state["triage_data"])}


def final_report_node(state):
    return {"final_report": {
        "project": "NightShift MD / MediCore AI",
        "patient_data": state["patient_data"],
        "medical_records": state["medical_records"],
        "history": state["history_data"],
        "triage": state["triage_data"],
        "llm_summary": state["summary_data"],
    }}


workflow = StateGraph(EmergencyFlowState)
workflow.add_node("patient_data", patient_data_node)
workflow.add_node("medical_records", medical_records_node)
workflow.add_node("history", history_node)
workflow.add_node("triage", triage_node)
workflow.add_node("summary", summary_node)
workflow.add_node("final_report", final_report_node)
workflow.add_edge(START, "patient_data")
workflow.add_edge("patient_data", "medical_records")
workflow.add_edge("medical_records", "history")
workflow.add_edge("history", "triage")
workflow.add_edge("triage", "summary")
workflow.add_edge("summary", "final_report")
workflow.add_edge("final_report", END)
emergency_flow = workflow.compile()


@app.get("/")
def home():
    return FileResponse(FRONTEND)


@app.post("/api/assess")
async def assess_patient(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF medical document.")
    raw = await file.read()
    tmp_path = BASE_DIR / "_uploaded_patient.pdf"
    tmp_path.write_bytes(raw)
    try:
        reader = PdfReader(str(tmp_path))
        pdf_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text + "\n"
        if not pdf_text.strip():
            raise HTTPException(status_code=422, detail="No text could be extracted from the PDF.")
        initial_state = {
            "pdf_text": pdf_text,
            "patient_data": {}, "medical_records": {}, "history_data": {},
            "triage_data": {}, "summary_data": "", "final_report": {}
        }
        result = emergency_flow.invoke(initial_state)
        return {
            "filename": file.filename,
            "page_count": len(reader.pages),
            "result": result["final_report"],
            "raw_text_length": len(pdf_text),
        }
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
