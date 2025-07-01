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


    # 📝 Log user query and response to log.json
    def log_interaction(user_input, result):
        try:
            with open("log.json", "r") as log_file:
                logs = json.load(log_file)
        except FileNotFoundError:
            logs = []

        logs.append({
            "query": user_input,
            "response": result
        })

        with open("log.json", "w") as log_file:
            json.dump(logs, log_file, indent=2)


    # Log after generating the response
    log_interaction(user_query, response)
    st.markdown(response)

def find_answer(query):
    for vuln in knowledge_base:
        if vuln["name"].lower() in query.lower():
            # Format prevention as bullet points if it's a list
            if isinstance(vuln["prevention"], list):
                prevention_bullets = "\n".join([f"- {item}" for item in vuln["prevention"]])
            else:
                prevention_bullets = vuln["prevention"]  # fallback for string

            return f"""### 🧠 {vuln['name']}

📌 **Description**  
{vuln['description']}

🛡️ **Prevention**
{prevention_bullets}
"""
    return "⚠️ Sorry, I don't know about that vulnerability."

