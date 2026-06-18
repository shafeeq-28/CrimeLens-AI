import google.generativeai as genai

import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_gemini_report(
    incident,
    crime_type,
    severity,
    department
):

    prompt = f"""
You are a police investigation assistant.

Complaint:
{incident}

Crime Type:
{crime_type}

Severity:
{severity}

Department:
{department}

Generate a professional investigation note
in 4-5 lines.
"""

    response = model.generate_content(
        prompt
    )

    return response.text