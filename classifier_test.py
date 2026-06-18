from ai_classifier import classify_crime

while True:

    complaint = input(
        "\nEnter Complaint: "
    )

    category, confidence = classify_crime(
        complaint
    )

    print()

    print(
        f"Predicted Crime Type: {category}"
    )

    print(
        f"Confidence: {confidence:.3f}"
    )