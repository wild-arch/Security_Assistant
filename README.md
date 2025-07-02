# 🛡️ SecureAssistant – AI Cybersecurity Helper

SecureAssistant is a simple, educational AI assistant that explains and simulates common web security vulnerabilities. Built with Python, Streamlit, and optional LangChain/OpenAI integration, it helps developers and students understand threats like SQL Injection, XSS, CSRF, and more.

---

## 🚀 Features

- 💬 Ask questions about known vulnerabilities (e.g. "What is SQL Injection?")
- ⚔️ Run `/simulate xss`, `/simulate sqli`, etc. to see how attacks work
- 🧠 Uses a JSON-based knowledge base (no need for constant API access)
- 📝 Logs all user queries, responses, and tags (`log.json`)
- 📊 Built-in query log viewer with filtering by tag (simulation, vulnerability, unknown)
- 🔧 Optional LangChain + OpenAI for fallback when local data is unavailable

---

🛡️ Security-Aware AI Assistant – Final Reflection  
Over the past 5 days, I built a lightweight AI assistant capable of answering questions about common web security vulnerabilities and simulating how these attacks might work. The assistant runs locally with a Streamlit interface and is powered by a JSON-based knowledge base and optional OpenAI + LangChain integration.

### What I built:
- A question-answering assistant focused on web vulnerabilities (SQLi, XSS, CSRF, etc.)
- A simulation feature using /simulate [vulnerability]
- A local log system (log.json) that stores all user queries, responses, and tags
- A web interface to interact with the assistant and view query history

### What I learned:
- Practical use of Streamlit for creating simple interactive dashboards
- Structuring knowledge in a JSON file for fast access and formatting
- Using LangChain to augment an assistant with LLMs (even though API limits stopped this)
- Implementing a simple but useful logging and visualization pipeline
- How to simulate security attacks in an educational and safe format

### What I’d improve:
- Add semantic search for more flexible question matching
- Integrate vector store (e.g. FAISS) for better long-term memory
- Improve the UI/UX and limit or collapse the query viewer
- Fully deploy the app using Render or Hugging Face Spaces

