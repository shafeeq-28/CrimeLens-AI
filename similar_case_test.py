from sentence_transformers import SentenceTransformer
from sentence_transformers import util

# Load model

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Existing complaints

complaints = [

    "My bike was stolen near Tambaram railway station",

    "A motorcycle theft occurred in Chromepet",

    "I received a fraudulent banking call",

    "Someone broke into my house and stole valuables",

    "Online scam caused financial loss",

    "Vehicle theft reported near GST Road"

]

# New complaint

new_complaint = (
    "Someone stole my motorcycle near Tambaram"
)

print()
print("NEW COMPLAINT:")
print(new_complaint)

print("\nGenerating embeddings...\n")

# Encode all complaints

complaint_embeddings = model.encode(
    complaints,
    convert_to_tensor=True
)

new_embedding = model.encode(
    new_complaint,
    convert_to_tensor=True
)

# Calculate similarities

similarities = util.cos_sim(
    new_embedding,
    complaint_embeddings
)

# Convert to list

scores = similarities[0].tolist()

# Combine complaint and score

results = list(
    zip(
        complaints,
        scores
    )
)

# Sort by similarity

results.sort(
    key=lambda x: x[1],
    reverse=True
)

print("TOP SIMILAR CASES\n")

for complaint, score in results:

    print(
        f"{score:.3f}  -->  {complaint}"
    )
