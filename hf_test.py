import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    import os

token = os.getenv("HF_TOKEN")
}

payload = {
    "inputs": """
    My bike was stolen yesterday near Tambaram railway station.
    I parked it outside the station and when I returned it was missing.
    """
}

response = requests.post(
    API_URL,
    headers=headers,
    json=payload
)

print(response.json())
