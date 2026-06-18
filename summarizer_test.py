from ai_summarizer import summarize_complaint

complaint = """
My motorcycle was parked near Tambaram railway station.
When I returned after work, I found it missing.
Nearby CCTV cameras may have recorded the theft.
I immediately searched the area but could not find the vehicle.
"""

summary = summarize_complaint(
    complaint
)

print("\nSUMMARY:\n")
print(summary)