from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

complaint1 = "My bike was stolen near Tambaram railway station"

complaint2 = "Someone stole my motorcycle near Tambaram"

complaint3 = "I received a bank fraud phone call"

embedding1 = model.encode(
    complaint1,
    convert_to_tensor=True
)

embedding2 = model.encode(
    complaint2,
    convert_to_tensor=True
)

embedding3 = model.encode(
    complaint3,
    convert_to_tensor=True
)

similarity_1_2 = util.cos_sim(
    embedding1,
    embedding2
)

similarity_1_3 = util.cos_sim(
    embedding1,
    embedding3
)

print()

print("Complaint 1:")
print(complaint1)

print()

print("Complaint 2:")
print(complaint2)

print()

print(
    "Similarity between Complaint 1 and Complaint 2:"
)

print(
    similarity_1_2.item()
)

print()

print("Complaint 3:")
print(complaint3)

print()

print(
    "Similarity between Complaint 1 and Complaint 3:"
)

print(
    similarity_1_3.item()
)