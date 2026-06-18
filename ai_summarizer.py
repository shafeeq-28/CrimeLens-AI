from sentence_transformers import SentenceTransformer
import re

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def summarize_complaint(text):

    sentences = re.split(
        r'[.!?]',
        text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    if len(sentences) <= 2:
        return text

    embeddings = model.encode(
        sentences
    )

    document_embedding = model.encode(
        [text]
    )[0]

    scores = []

    for i, embedding in enumerate(embeddings):

        similarity = (
            embedding @ document_embedding
        )

        scores.append(
            (
                similarity,
                sentences[i]
            )
        )

    scores.sort(
        reverse=True
    )

    top_sentences = [
        s[1]
        for s in scores[:2]
    ]

    return ". ".join(
        top_sentences
    ) + "."