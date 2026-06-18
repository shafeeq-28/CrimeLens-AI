from gemini_agent import generate_gemini_report

report = generate_gemini_report(
    "My bank account was hacked and money was stolen",
    "Cyber Crime",
    "High",
    "Cyber Crime Cell"
)

print(report)