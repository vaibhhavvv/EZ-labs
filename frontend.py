import streamlit as st
import requests

st.set_page_config(page_title="GenAI Document Assistant", layout="centered")

API_URL = "http://localhost:8000"  # Replace with deployed URL if needed

st.title("📄 GenAI Document Assistant")

# Upload document
st.header("1. Upload Document")
uploaded = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
doc_id = None

if uploaded:
    with st.spinner("Uploading and processing..."):
        files = {"file": uploaded.getvalue()}
        response = requests.post(f"{API_URL}/upload", files={"file": (uploaded.name, uploaded)})
        if response.status_code == 200:
            doc_id = response.json()["doc_id"]
            st.success("File uploaded!")

            # Show summary
            summary_res = requests.post(f"{API_URL}/summary", data={"doc_id": doc_id})
            st.subheader("🔍 Auto Summary")
            st.write(summary_res.json()["summary"])
        else:
            st.error("Upload failed")

if doc_id:
    st.header("2. Ask Anything")
    question = st.text_input("Enter your question")
    if st.button("Ask") and question:
        resp = requests.post(f"{API_URL}/ask", data={"doc_id": doc_id, "question": question})
        st.subheader("🧠 Answer")
        st.write(resp.json()["answer"])

    st.header("3. Challenge Me")
    if st.button("Get Questions"):
        resp = requests.post(f"{API_URL}/challenge", data={"doc_id": doc_id})
        st.subheader("🧩 Logic-Based Questions")
        st.session_state.questions = resp.json()["questions"]
        st.write(st.session_state.questions)

    if "questions" in st.session_state:
        st.subheader("📝 Your Answers")
        answers = []
        for i in range(3):
            ans = st.text_input(f"Answer {i+1}")
            answers.append(ans)

        if st.button("Evaluate"):
            eval_resp = requests.post(f"{API_URL}/challenge", data={"doc_id": doc_id, "user_answers": answers})
            st.subheader("📊 Evaluation")
            st.write(eval_resp.json()["evaluation"])
