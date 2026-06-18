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


def ask_legal_ai(question):

    query_embedding = model.encode(
        [question]
    )

    D, I = index.search(
        np.array(
            query_embedding,
            dtype="float32"
        ),
        k=3
    )

    retrieved_chunks = []

    for idx in I[0]:

        if idx < len(chunks):

            retrieved_chunks.append(
                chunks[idx]
            )

    context = "\n\n".join(
        retrieved_chunks
    )

    answer = f"""
Question:
{question}

Relevant Legal Information:

{context}

Recommended Actions:

1. Preserve any available evidence.
2. Report the incident to the appropriate authorities.
3. Keep records of communications and documents.
4. Follow official legal procedures when filing complaints.

Note:
This response is generated from the Criminal Case Assistant legal knowledge base.
"""

    return answer