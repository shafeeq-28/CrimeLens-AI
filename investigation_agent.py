def analyze_severity(
    crime_type,
    complaint_text
):

    text = complaint_text.lower()

    if crime_type == "Cyber Crime":

        if (
            "bank" in text
            or "money" in text
            or "account" in text
            or "stolen" in text
        ):
            return "High"

        return "Medium"

    elif crime_type == "Theft":

        if (
            "vehicle" in text
            or "bike" in text
            or "car" in text
        ):
            return "High"

        return "Medium"

    elif crime_type == "Assault":

        return "High"

    elif crime_type == "Missing Person":

        return "Critical"

    else:

        return "Medium"


def get_evidence_required(
    crime_type
):

    if crime_type == "Cyber Crime":

        return [
            "Screenshots",
            "Transaction IDs",
            "Email Records",
            "Chat Logs"
        ]

    elif crime_type == "Theft":

        return [
            "Purchase Bill",
            "Photos",
            "Witness Statements",
            "CCTV Footage"
        ]

    elif crime_type == "Fraud":

        return [
            "Bank Statements",
            "Transaction Records",
            "Screenshots"
        ]

    elif crime_type == "Assault":

        return [
            "Medical Reports",
            "Witness Statements",
            "Photos"
        ]

    else:

        return [
            "Supporting Documents"
        ]


def get_department(
    crime_type
):

    if crime_type == "Cyber Crime":

        return "Cyber Crime Cell"

    elif crime_type == "Fraud":

        return "Economic Offences Wing"

    elif crime_type == "Theft":

        return "Local Police Station"

    elif crime_type == "Assault":

        return "Law and Order Division"

    else:

        return "General Complaints Department"


def generate_investigation_report(
    crime_type,
    incident
):

    severity = analyze_severity(
        crime_type,
        incident
    )

    evidence = get_evidence_required(
        crime_type
    )

    department = get_department(
        crime_type
    )

    report = {
        "crime_type": crime_type,
        "severity": severity,
        "department": department,
        "evidence": evidence
    }

    return report