import google.generativeai as genai

genai.configure(
    import os

api_key = os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

response = model.generate_content(
    "Write a one-line police investigation note for a cyber crime complaint."
)

print(response.text)