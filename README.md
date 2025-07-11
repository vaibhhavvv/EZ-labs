# 🧠 GenAI Document Assistant

AI-powered assistant that reads user-uploaded documents (PDF/TXT), understands content deeply, and:

* Answers context-aware questions
* Asks logic-based questions
* Provides justification for every answer
* Generates concise summaries instantly

---

## 🚀 Features

* 📄 Upload PDF/TXT documents
* 🔍 Auto-summarization (≤150 words)
* 🤖 "Ask Anything" free-form Q\&A mode
* 🧩 "Challenge Me": Logic-based question generation and evaluation
* 📚 Context-anchored answers (with section/paragraph references)
* 📪 Postman collection for API testing

---

## 🧱 Architecture

```
            ┌────────────┐       ┌──────────────┐
Upload PDF →│ Streamlit  │←API→ │  FastAPI      │
Interact UI │ Frontend   │       │  Backend     │
            └────────────┘       └────┬─────────┘
                                     ↓
                           Extract Text / Call OpenAI
                                     ↓
                            Logic | Summary | Answers
```

* **Frontend**: Streamlit (minimal, interactive UI)
* **Backend**: FastAPI (handles file parsing, LLM prompts)
* **NLP Engine**: OpenAI GPT-3.5-Turbo (or local LLM via API)
* **PDF Parser**: PyMuPDF

---

## 🧰 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/genai-doc-assistant.git
cd genai-doc-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

```bash
export OPENAI_API_KEY=your-key-here
```

### 4. Run Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

### 5. Run Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

### 6. Test with Postman

* Import `postman/GenAI.postman_collection.json`
* Test endpoints: `/upload`, `/summary`, `/ask`, `/challenge`

---

## 📂 Project Structure

```
.
├── backend/
│   └── main.py            # FastAPI backend
├── frontend/
│   └── app.py             # Streamlit UI
├── postman/
│   └── GenAI.postman_collection.json
├── requirements.txt       # Dependencies
└── README.md
```

---

## 📊 Evaluation Criteria (as per assignment)

| Criteria                        | Weight |
| ------------------------------- | ------ |
| Accuracy + Justification        | 30%    |
| Challenge Mode Effectiveness    | 20%    |
| UI/UX                           | 15%    |
| Code Quality + Docs             | 15%    |
| Creativity (Memory, Highlights) | 10%    |
| Context Use (Low Hallucination) | 10%    |

---

## 📎 Future Enhancements

* 🔁 Add memory for follow-up questions
* 🖍 Highlight supporting snippets in answer
* 💾 Store user sessions and answers

---

**Author**: Vaibhav Srivastava
**Submission for**: GenAI Internship – Smart Assistant Task
