import sqlite3


def find_similar_cases(
    new_complaint,
    current_complaint_id=None
):

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

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

    cursor.execute(
        """
        SELECT id,
               incident
        FROM complaints
        WHERE crime_type = ?
        """,
        (crime_type,)
    )

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        if row[0] != current_complaint_id:

            results.append(
                (
                    row[0],
                    row[1],
                    1.0
                )
            )

    return results[:3]