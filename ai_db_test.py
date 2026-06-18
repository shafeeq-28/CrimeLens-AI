from ai_search import find_similar_cases

query = input(
    "Enter complaint: "
)

results = find_similar_cases(
    query
)

print()

print("TOP MATCHES")

print()

for complaint_id, text, score in results:

    print(
        f"ID: {complaint_id}"
    )

    print(
        f"Score: {score:.3f}"
    )

    print(
        f"Complaint: {text}"
    )

    print("-" * 50)