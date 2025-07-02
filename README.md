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


