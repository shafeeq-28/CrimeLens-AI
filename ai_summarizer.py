def summarize_complaint(text):

    sentences = text.split(".")

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if len(sentences) <= 2:
        return text

    return ". ".join(sentences[:2]) + "."