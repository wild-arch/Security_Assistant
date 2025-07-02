import json

# Load vulnerabilities
with open("vulnerabilities.json", "r") as vuln_file:
    knowledge_base = json.load(vuln_file)

# Load log.json
with open("log.json", "r") as log_file:
    logs = json.load(log_file)

# Patch each entry
for entry in logs:
    if "tag" not in entry:
        query = entry["query"].lower()
        if query.startswith("/simulate"):
            entry["tag"] = "simulation"
        elif any(vuln["name"].lower() in query for vuln in knowledge_base):
            entry["tag"] = "vulnerability"
        else:
            entry["tag"] = "unknown"

# Save back
with open("log.json", "w") as log_file:
    json.dump(logs, log_file, indent=2)

print("✅ log.json patched with missing tags.")
