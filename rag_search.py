from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "legal_index.faiss"
)

with open(
    "chunks.txt",
    "r",
    encoding="utf-8"
) as file:

    chunks = file.read().split(
        "\n===CHUNK===\n"
    )

question = input(
    "Ask Question: "
)

query_embedding = model.encode(
    [question]
)

D, I = index.search(
    np.array(
        query_embedding,
        dtype="float32"
    ),
    k=1
)

print("\nAnswer:\n")

print(
    chunks[I[0][0]]
)