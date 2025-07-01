import streamlit as st
import json

# 🎯 App title and description
st.title("🛡️ Security-Aware AI Assistant")
st.write("Ask me about common web vulnerabilities, or try `/simulate xss`.")

# 📚 Load the vulnerability knowledge base from JSON
def load_knowledge():
    with open("vulnerabilities.json", "r") as file:
        return json.load(file)

# Load the knowledge base once
knowledge_base = load_knowledge()

# 🔍 Find an answer to a user question based on the knowledge base
def find_answer(query):
    for vuln in knowledge_base:
        if vuln["name"].lower() in query.lower():
            return f"### 🧠 {vuln['name']}\n\n📌 {vuln['description']}\n\n🛡️ **Prevention:** {vuln['prevention']}"
    return "⚠️ Sorry, I don't know about that vulnerability."

# 🎭 Simulate how a vulnerability works (basic text explanation)
def simulate_vulnerability(query):
    for vuln in knowledge_base:
        if vuln["name"].lower() in query.lower():
            return f"🚨 **Simulating {vuln['name']} Attack:**\n\n{vuln['simulation']}"
    return "⚠️ I don't have a simulation for that vulnerability."

# 🧠 Process user input
user_query = st.text_input("Type your question or a /simulate command:")

if user_query:
    if user_query.startswith("/simulate"):
        # Get the part after /simulate (e.g., "xss")
        sim_target = user_query.replace("/simulate", "").strip().lower()
        response = simulate_vulnerability(sim_target)
    else:
        response = find_answer(user_query)

    st.markdown(response)
