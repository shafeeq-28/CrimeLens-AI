from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
import db
from ai_search import find_similar_cases
from ai_classifier import classify_crime
from ai_summarizer import summarize_complaint
from fastapi.staticfiles import StaticFiles
from gemini_agent import generate_gemini_report
from investigation_agent import (
    analyze_severity,
    generate_investigation_report
)
from send_email import (
    send_complaint_email,
    send_status_update_email
)
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templatess")

CURRENT_USER = None

LAST_REPORT = None

# --------------------------------
# Models
# --------------------------------

class ComplaintAnalysis(BaseModel):
    complaint: str


class StatusUpdate(BaseModel):
    status: str


# --------------------------------
# Demo Users
# --------------------------------

USERS = {
    "user1": "123",
    "user2": "123",
    "police": "admin123"
}


# --------------------------------
# Crime Detection
# --------------------------------

def detect_crime_type(incident):

    text = incident.lower()

    if "stolen" in text or "theft" in text:
        return "Theft"

    elif "fraud" in text or "scam" in text:
        return "Fraud"

    elif "attack" in text or "assault" in text:
        return "Assault"

    elif "damage" in text:
        return "Property Damage"

    else:
        return "Unknown"


# --------------------------------
# Login
# --------------------------------

@app.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    global CURRENT_USER

    if username == "police" and password == "admin123":

        CURRENT_USER = "police"

        return RedirectResponse(
            url="/police-dashboard",
            status_code=303
        )

    elif username in USERS and USERS[username] == password:

        CURRENT_USER = username

        return RedirectResponse(
            url="/citizen-dashboard",
            status_code=303
        )

    return {
        "message": "Invalid Username or Password"
    }


# --------------------------------
# Citizen Dashboard
# --------------------------------

@app.get("/citizen-dashboard")
def citizen_dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="citizen_dashboard.html"
    )


# --------------------------------
# Police Dashboard
# --------------------------------

@app.get("/police-dashboard")
def police_dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="police_dashboard.html"
    )

# --------------------------------
# Search Crime Page
# --------------------------------

@app.get("/search-crime-page")
def search_crime_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="search_crime.html"
    )


@app.post("/search-crime")
def search_crime(
    request: Request,
    crime_type: str = Form(...)
):

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM complaints
        WHERE crime_type = ?
        """,
        (crime_type,)
    )

    complaints = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="crime_results.html",
        context={
            "request": request,
            "complaints": complaints
        }
    )
# --------------------------------
# Analytics Dashboard
# --------------------------------

@app.get("/analytics")
def analytics(request: Request):

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    # Total complaints
    cursor.execute(
        "SELECT COUNT(*) FROM complaints"
    )
    total_complaints = cursor.fetchone()[0]

    # Pending cases
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM complaints
        WHERE status = 'Pending'
        """
    )
    pending_cases = cursor.fetchone()[0]

    # Closed cases
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM complaints
        WHERE status = 'Closed'
        """
    )
    closed_cases = cursor.fetchone()[0]

    # Theft cases
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM complaints
        WHERE crime_type = 'Theft'
        """
    )
    theft_cases = cursor.fetchone()[0]

    # Cyber Crime cases
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM complaints
        WHERE crime_type = 'Cyber Crime'
        """
    )
    cyber_cases = cursor.fetchone()[0]

    # Fraud cases
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM complaints
        WHERE crime_type = 'Fraud'
        """
    )
    fraud_cases = cursor.fetchone()[0]

    # Most common crime type

    cursor.execute(
        """
        SELECT crime_type, COUNT(*)
        FROM complaints
        GROUP BY crime_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """
    )

    crime_row = cursor.fetchone()

    if crime_row:
        most_common_crime = crime_row[0]
    else:
        most_common_crime = "N/A"

    # Most active location

    cursor.execute(
        """
        SELECT location, COUNT(*)
        FROM complaints
        GROUP BY location
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """
    )

    location_row = cursor.fetchone()

    if location_row:
        most_active_location = location_row[0]
    else:
        most_active_location = "N/A"

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "request": request,
            "total_complaints": total_complaints,
            "pending_cases": pending_cases,
            "closed_cases": closed_cases,
            "theft_cases": theft_cases,
            "cyber_cases": cyber_cases,
            "fraud_cases": fraud_cases,
            "most_common_crime": most_common_crime,
            "most_active_location": most_active_location
        }
    )

# --------------------------------
# Police Complaints Page
# --------------------------------

@app.get("/police-complaints")
def police_complaints(request: Request):

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints"
    )

    rows = cursor.fetchall()

    complaints = []

    for row in rows:

        row = list(row)

        summary = summarize_complaint(
            row[3]
        )

        row.append(summary)

        complaints.append(row)

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="police_complaints.html",
        context={
            "request": request,
            "complaints": complaints
        }
    )
# --------------------------------
# Similar Cases
# --------------------------------

@app.get("/similar-cases/{complaint_id}")
def similar_cases(
    complaint_id: int,
    request: Request
):

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT incident
        FROM complaints
        WHERE id = ?
        """,
        (complaint_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:

        return {
            "message": "Complaint not found"
        }

    incident = row[0]

    cases = find_similar_cases(
        incident,
        complaint_id
    )

    return templates.TemplateResponse(
        request=request,
        name="similar_cases.html",
        context={
            "request": request,
            "cases": cases
        }
    )

# --------------------------------
# Update Status Page
# --------------------------------

@app.get("/update-status-page/{complaint_id}")
def update_status_page(
    complaint_id: int,
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="update_status.html"
    )

@app.post("/update-status-page/{complaint_id}")
def save_status(
    complaint_id: int,
    status: str = Form(...)
):

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT email
        FROM complaints
        WHERE id = ?
        """,
        (complaint_id,)
    )

    row = cursor.fetchone()

    if row:
        receiver_email = row[0]
    else:
        receiver_email = None

    cursor.execute(
        """
        UPDATE complaints
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            complaint_id
        )
    )

    conn.commit()
    conn.close()

    display_id = (
        f"CR2026-{complaint_id:03d}"
    )

    if receiver_email:

        try:

            send_status_update_email(
                receiver_email,
                display_id,
                status
            )

            print(
                "Status update email sent!"
            )

        except Exception as e:

            print(
                "Status Email Error:",
                e
            )

    return RedirectResponse(
        url="/police-complaints",
        status_code=303
    )
# --------------------------------
# Complaint Form
# --------------------------------

@app.get("/complaint-form")
def complaint_form(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="complaint_form.html"
    )


# --------------------------------
# My Complaints
# --------------------------------

@app.get("/my-complaints")
def my_complaints(request: Request):

    global CURRENT_USER

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM complaints
        WHERE username = ?
        """,
        (CURRENT_USER,)
    )

    complaints = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="my_complaints.html",
        context={
            "request": request,
            "complaints": complaints
        }
    )


# --------------------------------
# Success
# --------------------------------

@app.get("/success")
def success(request: Request):

    global LAST_REPORT

    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "request": request,
            "report": LAST_REPORT
        }
    )


# --------------------------------
# Add Complaint
# --------------------------------

@app.post("/complaint")
def create_complaint(
    name: str = Form(...),
    email: str = Form(...),
    incident: str = Form(...),
    location: str = Form(...),
    date: str = Form(...)
):

    global CURRENT_USER
    global LAST_REPORT

    try:

        print("STEP 1")

        crime_type, confidence = classify_crime(
            incident
        )

        print("STEP 2")

        LAST_REPORT = generate_investigation_report(
            crime_type,
            incident
        )

        print("STEP 3")

        severity = analyze_severity(
            crime_type,
            incident
        )

        print("STEP 4")

        try:

            LAST_REPORT["gemini_notes"] = generate_gemini_report(
                incident,
                crime_type,
                severity,
                LAST_REPORT["department"]
            )

        except Exception as e:

            print(
                "Gemini Error:",
                e
            )

            LAST_REPORT["gemini_notes"] = (
                "Gemini report unavailable."
            )

        print("STEP 5")

        status = "Pending"

        formal_complaint = f"""
The complainant {name} reported that
{incident} at {location}
on {date}.
"""

        conn = sqlite3.connect(
            "complaints.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO complaints
            (
                username,
                name,
                email,
                incident,
                location,
                date,
                crime_type,
                status,
                formal_complaint
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                CURRENT_USER,
                name,
                email,
                incident,
                location,
                date,
                crime_type,
                status,
                formal_complaint
            )
        )

        complaint_id = cursor.lastrowid

        conn.commit()
        conn.close()

        print("STEP 6")

        display_id = (
            f"CR2026-{complaint_id:03d}"
        )

        try:

            send_complaint_email(
                email,
                display_id,
                crime_type,
                status
            )

        except Exception as e:

            print(
                "Email Error:",
                e
            )

        print("STEP 7")

        return RedirectResponse(
            url="/success",
            status_code=303
        )

    except Exception as e:

        print(
            "COMPLAINT ROUTE ERROR:",
            e
        )

        return {
            "error": str(e)
        }

# --------------------------------
# View All Complaints API
# --------------------------------

@app.get("/complaints")
def get_complaints():

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints"
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------
# Search By Crime Type
# --------------------------------

@app.get("/search-by-crime/{crime_type}")
def search_by_crime(crime_type: str):

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM complaints
        WHERE crime_type = ?
        """,
        (crime_type,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------
# Update Status API
# --------------------------------

@app.put("/update-status/{complaint_id}")
def update_status(
    complaint_id: int,
    status_data: StatusUpdate
):

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT email
        FROM complaints
        WHERE id = ?
        """,
        (complaint_id,)
    )

    row = cursor.fetchone()

    if row:
        receiver_email = row[0]
    else:
        receiver_email = None

    cursor.execute(
        """
        UPDATE complaints
        SET status = ?
        WHERE id = ?
        """,
        (
            status_data.status,
            complaint_id
        )
    )

    conn.commit()
    conn.close()

    display_id = (
        f"CR2026-{complaint_id:03d}"
    )

    if receiver_email:

        try:

            send_status_update_email(
                receiver_email,
                display_id,
                status_data.status
            )

        except Exception as e:

            print(
                "Status Email Error:",
                e
            )

    return {
        "message": f"Complaint {complaint_id} updated",
        "new_status": status_data.status
    }


# --------------------------------
# Analyze Complaint
# --------------------------------

@app.post("/analyze-complaint")
def analyze_complaint(data: ComplaintAnalysis):

    crime_type = detect_crime_type(
        data.complaint
    )

    return {
        "crime_type": crime_type,
        "location": "Not Detected Yet",
        "summary": data.complaint
    }


@app.get("/legal-ai")
def legal_ai_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="rag_assistant.html",
        context={
            "request": request,
            "answer": None
        }
    )


@app.get("/agent-report-test")
def agent_report_test(
    request: Request
):

    report = generate_investigation_report(
        "Cyber Crime",
        "My bank account was hacked and money was stolen"
    )

    return templates.TemplateResponse(
        request=request,
        name="agent_report.html",
        context={
            "request": request,
            "report": report
        }
    )
