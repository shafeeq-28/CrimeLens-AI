from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

CRIME_CATEGORIES = {

    "Theft":
    "bike theft, vehicle theft, robbery, stealing money, stealing property, stolen items",

    "Fraud":
    "bank fraud, financial scam, fake call, cheating, credit card fraud, online fraud",

    "Assault":
    "physical attack, violence, beating, injury, assaulting a person",

    "Property Damage":
    "damaging property, vandalism, breaking windows, damaging vehicle, damaging building",

    "Cyber Crime":
    "phone hacked, email hacked, social media hacked, cyber attack, phishing, account hacked, online hacking",

    "Missing Person":
    "missing child, missing person, family member disappeared, person not found",

    "Domestic Violence":
    "domestic abuse, family violence, husband abuse, wife abuse, household violence",

    "Drug Offense":
    "illegal drugs, narcotics, drug trafficking, drug selling, drug possession"
}


def classify_crime(complaint_text):

    category_names = list(
        CRIME_CATEGORIES.keys()
    )

    category_descriptions = list(
        CRIME_CATEGORIES.values()
    )

    category_embeddings = model.encode(
        category_descriptions,
        convert_to_tensor=True
    )

    complaint_embedding = model.encode(
        complaint_text,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        complaint_embedding,
        category_embeddings
    )[0]

    best_index = similarities.argmax().item()

    predicted_category = category_names[
        best_index
    ]

    confidence = float(
        similarities[best_index]
    )

    return predicted_category, confidence