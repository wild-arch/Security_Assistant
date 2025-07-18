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
from langchain.llms import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

import vectorstore

# llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.3}, huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

llm = OllamaLLM(model="llama3.2:1b")

template = """
You are a smart cybersecurity professional,.

Your task is to:
1. Analyze the user's question 
2. Explain your reasoning step-by-step

Only answer questions that are related to cybersecurity vulnerabilities, if the question is unrelated, respond "The question provided is outside my scope"
You are only to use the provided context
Question: {question}

You will be provided with a context to help answer the question: {context}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

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

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True  # optional

)


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
    _response=chain.invoke({"question": query,"context":response})
    print(_response)


    return _response


# 🎭 Simulate vulnerabilities
def simulate_vulnerability(query):
    query_lower = query.lower()
    for vuln in knowledge_base:
        # Check both the name and the keywords
        if vuln["name"].lower() in query_lower or any(k.lower() in query_lower for k in vuln.get("keywords", [])):
            return f"""
<div style="background-color:#1f1f1f; padding:15px; border-radius:10px; color:#f2f2f2;">
<h4>🚨 Simulating {vuln['name']} Attack</h4>
<p>{vuln['simulation']}</p>
</div>
"""
    return """
<div style="background-color:#1f1f1f; padding:15px; border-radius:10px; color:#ffdddd;">
⚠️ I don't have a simulation for that vulnerability.
</div>
"""


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
        st.markdown(f"<div style='background-color:#ffebeb;padding:10px;border-radius:10px'>{response}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown(response, unsafe_allow_html=True)

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
