import streamlit as st
import json
from dotenv import load_dotenv
import os

# 🧪 Load .env for OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 🔗 LangChain setup
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = OpenAI(openai_api_key=openai_api_key, temperature=0.3)

prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful cybersecurity assistant. Answer the following question:\n{question}"
)

chain = LLMChain(llm=llm, prompt=prompt)

# 🎯 Streamlit UI
st.title("🛡️ Security-Aware AI Assistant")
st.write("Ask me about common web vulnerabilities, or try `/simulate xss`.")

# 📚 Load vulnerabilities
def load_knowledge():
    with open("vulnerabilities.json", "r") as file:
        return json.load(file)

knowledge_base = load_knowledge()

# 🔍 Answer from local knowledge base
def find_answer(query):
    for vuln in knowledge_base:
        if vuln["name"].lower() in query.lower():
            # Format prevention bullets
            if isinstance(vuln["prevention"], list):
                prevention_bullets = "\n".join([f"- {item}" for item in vuln["prevention"]])
            else:
                prevention_bullets = vuln["prevention"]

            return f"""### 🧠 {vuln['name']}

📌 **Description**  
{vuln['description']}

🛡️ **Prevention**  
{prevention_bullets}
"""
    return "⚠️ Sorry, I don't know about that vulnerability."

# 🎭 Simulation output
def simulate_vulnerability(query):
    for vuln in knowledge_base:
        if vuln["name"].lower() in query.lower():
            return f"🚨 **Simulating {vuln['name']} Attack:**\n\n{vuln['simulation']}"
    return "⚠️ I don't have a simulation for that vulnerability."

# 📝 Logging interaction
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

# 🧠 Main query input
user_query = st.text_input("Type your question or a /simulate command:")

if user_query:
    if user_query.startswith("/simulate"):
        sim_target = user_query.replace("/simulate", "").strip().lower()
        response = simulate_vulnerability(sim_target)
    else:
        # Try local knowledge base first
        answer = find_answer(user_query)

        # If not found, use LangChain/GPT
        if "Sorry" in answer:
            response = "⚠️ I don't know about that yet. Try a known vulnerability like SQLi or XSS."
        else:
            response = answer

    # Output + log
    st.markdown(response)
    log_interaction(user_query, response)
