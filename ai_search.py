from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import sqlite3


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def find_similar_cases(
    new_complaint,
    current_complaint_id=None
):

    conn = sqlite3.connect(
        r"C:\Users\shafeeq\complaints.db"
    )

    cursor = conn.cursor()

    # Get current complaint's crime type

    cursor.execute(
        """
        SELECT crime_type
        FROM complaints
        WHERE id = ?
        """,
        (current_complaint_id,)
    )

    crime_row = cursor.fetchone()

    if not crime_row:
        conn.close()
        return []

    crime_type = crime_row[0]

    # Fetch only same crime type complaints

    cursor.execute(
        """
        SELECT id, incident
        FROM complaints
        WHERE crime_type = ?
        """,
        (crime_type,)
    )

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        return []

    complaint_ids = []
    complaint_texts = []

    for row in rows:

        complaint_ids.append(
            row[0]
        )

        complaint_texts.append(
            row[1]
        )

    database_embeddings = model.encode(
        complaint_texts,
        convert_to_tensor=True
    )

    query_embedding = model.encode(
        new_complaint,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        query_embedding,
        database_embeddings
    )[0]

    results = []

    for i, score in enumerate(similarities):

        if complaint_ids[i] == current_complaint_id:
            continue

        results.append(
            (
                complaint_ids[i],
                complaint_texts[i],
                float(score)
            )
        )

    results.sort(
        key=lambda x: x[2],
        reverse=True
    )

    return results[:3]