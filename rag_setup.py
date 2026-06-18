from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

with open(
    "legal_docs/legal_guide.txt",
    "r",
    encoding="utf-8"
) as file:

    text = file.read()

chunks = text.split("\n\n")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    chunks
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    np.array(
        embeddings,
        dtype="float32"
    )
)

faiss.write_index(
    index,
    "legal_index.faiss"
)

with open(
    "chunks.txt",
    "w",
    encoding="utf-8"
) as file:

    for chunk in chunks:

        file.write(
            chunk + "\n===CHUNK===\n"
        )

print(
    "FAISS index created successfully!"
)