
import os
import json
from pathlib import Path
from typing import Optional
import pdfplumber
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
_model: Optional[SentenceTransformer] = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def score_resume(job_description: str, resume_text: str) -> float:
    model = get_model()
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    score = util.cos_sim(jd_embedding, resume_embedding).item()
    return round(score * 100, 2)


def screen_resumes(job_description: str, resumes_dir: str) -> list[dict]:
    resumes_path = Path(resumes_dir)
    pdf_files = list(resumes_path.glob("*.pdf"))

    if not pdf_files:
        return []

    results = []
    for pdf_file in pdf_files:
        try:
            text = extract_text_from_pdf(str(pdf_file))
            if not text:
                continue
            score = score_resume(job_description, text)
            results.append({
                "filename": pdf_file.name,
                "score": score,
                "preview": text[:300].replace("\n", " ") + "..."
            })
        except Exception as e:
            results.append({
                "filename": pdf_file.name,
                "score": 0.0,
                "preview": f"Error reading file: {str(e)}"
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def save_results(results: list[dict], output_path: str):
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)