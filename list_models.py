import google.generativeai as genai

genai.configure(
    import os

api_key = os.getenv("GEMINI_API_KEY")
)

for model in genai.list_models():

    print(model.name)

    if "generateContent" in model.supported_generation_methods:
        print("  -> supports generateContent")