from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import fitz  # PyMuPDF
import os
import uuid
import openai

app = FastAPI()

# CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store uploaded docs
documents = {}

# Set your OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Read PDF text
def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    ext = file.filename.split(".")[-1]
    if ext == "pdf":
        text = extract_text_from_pdf(content)
    elif ext == "txt":
        text = content.decode("utf-8")
    else:
        return JSONResponse(content={"error": "Only PDF and TXT allowed."}, status_code=400)

    doc_id = str(uuid.uuid4())
    documents[doc_id] = text
    return {"doc_id": doc_id}

@app.post("/summary")
async def summarize(doc_id: str = Form(...)):
    text = documents.get(doc_id, "")[:3000]  # truncate to fit context
    prompt = f"Summarize the following document in under 150 words:\n{text}"
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"summary": resp.choices[0].message.content.strip()}

@app.post("/ask")
async def ask_question(doc_id: str = Form(...), question: str = Form(...)):
    text = documents.get(doc_id, "")[:3000]
    prompt = f"Answer this question based on the document:\n\nDocument:\n{text}\n\nQuestion: {question}\n\nProvide the answer with justification and section reference."
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": resp.choices[0].message.content.strip()}

@app.post("/challenge")
async def challenge_user(doc_id: str = Form(...), user_answers: List[str] = Form([])):
    text = documents.get(doc_id, "")[:3000]
    q_prompt = f"Create 3 logic/comprehension questions based on the document."
    q_resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": q_prompt + '\n\n' + text}]
    )
    questions = q_resp.choices[0].message.content.strip()

    # If answers are provided, evaluate them (simulate for now)
    if user_answers:
        eval_prompt = f"Evaluate these answers to the questions based on the document:\n\n{text}\n\nAnswers: {user_answers}\nGive score and explanation."
        eval_resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": eval_prompt}]
        )
        return {"evaluation": eval_resp.choices[0].message.content.strip()}

    return {"questions": questions}
