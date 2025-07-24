# 🛡️ SecureAssistant – AI Cybersecurity Helper

**SecureAssistant** is a lightweight AI assistant that explains and simulates common web security vulnerabilities. Built using **Python**, **Streamlit**, and **LangChain** with free local components, it helps developers and students understand threats like **SQL Injection**, **XSS**, **CSRF**, and more — without needing API access or cloud credits.

---

## 🚀 Features

- 💬 Ask questions about known vulnerabilities (e.g. "What is SQL Injection?")
- ⚔️ Run `/simulate xss`, `/simulate sqli`, etc. to see how attacks might work
- 🧠 Uses a local JSON knowledge base + FAISS vector search for fast retrieval
- 📝 Logs all user queries, responses, and tags to `log.json`
- 📊 Built-in query log viewer with tag filtering (`simulation`, `vulnerability`, `unknown`)
- 🔍 Uses HuggingFace embeddings (`all-MiniLM-L6-v2`) for free semantic search

---

## 🛠️ Tech Stack

- **LangChain** for RAG (Retrieval-Augmented Generation)
- **FAISS** for local vector storage and retrieval
- **HuggingFace Embeddings** for free, local embeddings
- **Streamlit** for the interactive web UI
- **JSON** for structured knowledge base and logs

---

## 📁 File Overview

- `app.py` – Main Streamlit app
- `vulnerabilities.json` – Your cybersecurity knowledge base
- `log.json` – All interactions and tags stored here
- `patch_logs.py` – Retroactively tags previous logs if needed
- `requirements.txt` – Minimal dependencies 

---

## 🧠 Final Reflection

### What I built:
- A question-answering cybersecurity assistant focused on common web vulnerabilities
- A simulation feature (`/simulate`) to demonstrate how attacks might work
- A logging system with tagging for each interaction
- A simple, responsive UI using Streamlit

### What I learned:
- How to build RAG systems using LangChain and FAISS 
- Using HuggingFace embeddings for semantic document search
- Structuring and querying local knowledge bases
- Creating educational simulations of security attacks
- Implementing local logging and dashboard-style query review

### What I’d improve:
- Replace text-only responses with code snippets or diagrams
- Improve UI for better clarity (collapse logs, add icons, search bar)
- Add full deployment (Render, HuggingFace Spaces)
- Add feedback system or user ratings for answers

---

## ✅ How to Run Locally

```bash
git clone https://github.com/wild-arch/Security_Assistant
cd SecureAssistant
pip install -r requirements.txt
streamlit run app.py

# As far as am concerned