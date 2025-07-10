import json

# Load vulnerabilities
with open("vulnerabilities.json", "r") as vuln_file:
    knowledge_base = json.load(vuln_file)

# Load existing logs
try:
    with open("log.json", "r") as log_file:
        logs = json.load(log_file)
except FileNotFoundError:
    print("⚠️ log.json not found.")
    logs = []

# Patch missing tags
patched = False
for entry in logs:
    if "tag" not in entry:
        query = entry["query"].lower()
        if query.startswith("/simulate"):
            entry["tag"] = "simulation"
        elif any(vuln["name"].lower() in query for vuln in knowledge_base):
            entry["tag"] = "vulnerability"
        else:
            entry["tag"] = "unknown"
        patched = True

# Save if any were patched
if patched:
    with open("log.json", "w") as log_file:
        json.dump(logs, log_file, indent=2)
    print("✅ log.json patched with missing tags.")
else:
    print("ℹ️ No missing tags found. log.json already up-to-date.")
