import streamlit as st
import json
import os
from dotenv import load_dotenv

# 🧪 Load environment variables (optional if needed)
load_dotenv()

# 🔗 LangChain setup (Free + Local)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA


# 🎯 Streamlit UI
st.title("🛡️ Security-Aware AI Assistant ")
st.write("Ask me about common web vulnerabilities, or try `/simulate xss`.")

# 📚 Load vulnerabilities
def load_knowledge():
    with open("vulnerabilities.json", "r") as file:
        return json.load(file)

knowledge_base = load_knowledge()

# 🧠 Vector Store Setup
@st.cache_resource
def load_vectorstore():
    docs = []
    for vuln in knowledge_base:
        content = f"""Name: {vuln['name']}
Description: {vuln['description']}
Prevention: {vuln['prevention']}"""
        docs.append(Document(page_content=content, metadata={"source": vuln["name"]}))

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

vectorstore = load_vectorstore()

# 🧠 Simple Retrieval
def simple_rag(query):
    docs = vectorstore.similarity_search(query, k=2)
    if not docs:
        return "⚠️ Sorry, I couldn't find any info on that."
    response = "### Retrieved Info:\n"
    for i, doc in enumerate(docs, 1):
        name = doc.metadata.get("source", f"Result {i}")
        content = doc.page_content
        response += f"**Chunk {i}:**\n{doc.page_content}\n\n"
    return response

# 🎭 Simulate vulnerabilities
def simulate_vulnerability(query):
    for vuln in knowledge_base:
        name_lower = vuln["name"].lower()
        name_short = name_lower.split("(")[0].strip()
        if name_lower in query.lower() or name_short in query.lower():
            return f"🚨 **Simulating {vuln['name']} Attack:**\n\n{vuln['simulation']}"
    return "⚠️ I don't have a simulation for that vulnerability."

# 📝 Logging
def log_interaction(user_input, result):
    try:
        with open("log.json", "r") as log_file:
            logs = json.load(log_file)
    except FileNotFoundError:
        logs = []

    for entry in logs:
        if entry["query"].lower() == user_input.lower() and entry["response"] == result:
            return  # avoid duplicate

    if user_input.startswith("/simulate"):
        tag = "simulation"
    elif any(vuln["name"].lower() in user_input.lower() for vuln in knowledge_base):
        tag = "vulnerability"
    else:
        tag = "unknown"

    logs.append({
        "query": user_input,
        "response": result,
        "tag": tag
    })

    with open("log.json", "w") as log_file:
        json.dump(logs, log_file, indent=2)

# 🧠 Main interaction
user_query = st.text_input("Type your question or a /simulate command:")

if user_query:
    if user_query.startswith("/simulate"):
        sim_target = user_query.replace("/simulate", "").strip().lower()
        response = simulate_vulnerability(sim_target)
    else:
        response = simple_rag(user_query)

    if "🚨" in response:
        st.markdown(f"<div style='background-color:#ffebeb;padding:10px;border-radius:10px'>{response}</div>", unsafe_allow_html=True)
    else:
        st.markdown(response)

    log_interaction(user_query, response)

# 📊 Log Viewer
st.markdown("---")
st.subheader("📊 Query Log Viewer")

try:
    with open("log.json", "r") as file:
        logs = json.load(file)
except FileNotFoundError:
    logs = []

MAX_LOGS = 2
tag_filter = st.selectbox("Filter by tag", options=["all", "simulation", "vulnerability", "unknown"])

if tag_filter != "all":
    logs = [log for log in logs if log["tag"] == tag_filter]

for log in reversed(logs[-MAX_LOGS:]):
    st.markdown(f"""
**🗨️ Query:** `{log['query']}`  
**🏷️ Tag:** `{log.get('tag', 'not-tagged')}`  
**📤 Response:**  
{log['response']}
---
""")