CRIME_CATEGORIES = {

    "Theft": [
        "theft",
        "stolen",
        "robbery",
        "bike",
        "car",
        "vehicle"
    ],

    "Fraud": [
        "fraud",
        "scam",
        "cheating",
        "fake call",
        "fake website"
    ],

    "Assault": [
        "attack",
        "assault",
        "beaten",
        "violence",
        "injury"
    ],

    "Property Damage": [
        "damage",
        "vandalism",
        "broken"
    ],

    "Cyber Crime": [
        "hack",
        "hacked",
        "phishing",
        "account hacked",
        "email hacked",
        "bank account hacked"
    ]
}


def classify_crime(complaint_text):

    text = complaint_text.lower()

    for category, keywords in CRIME_CATEGORIES.items():

        for keyword in keywords:

            if keyword in text:

                return category, 0.95

    return "Unknown", 0.50