import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "criminalcaseassistant7@gmail.com"

APP_PASSWORD = "ekxenknbjawhoyxh"


def send_test_email(receiver_email):

    msg = EmailMessage()

    msg["Subject"] = "Criminal Case Assistant - Test Email"

    msg["From"] = SENDER_EMAIL

    msg["To"] = receiver_email

    msg.set_content(
        """
Hello,

This is a test email from the Criminal Case Assistant project.

Email notifications are working successfully.

Regards,
Criminal Case Assistant
        """
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)

    print("Email sent successfully!")


def send_complaint_email(
    receiver_email,
    complaint_id,
    crime_type,
    status
):

    msg = EmailMessage()

    msg["Subject"] = (
        f"Complaint Registered - {complaint_id}"
    )

    msg["From"] = SENDER_EMAIL

    msg["To"] = receiver_email

    msg.set_content(
        f"""
Complaint Registered Successfully

Complaint ID: {complaint_id}

Crime Type: {crime_type}

Current Status: {status}

Thank you for using Criminal Case Assistant.

Regards,
Criminal Case Assistant
        """
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)

    print(
        "Complaint email sent successfully!"
    )
def send_status_update_email(
    receiver_email,
    complaint_id,
    new_status
):

    msg = EmailMessage()

    msg["Subject"] = (
        f"Status Updated - {complaint_id}"
    )

    msg["From"] = SENDER_EMAIL

    msg["To"] = receiver_email

    msg.set_content(
        f"""
Complaint Status Updated

Complaint ID: {complaint_id}

New Status: {new_status}

Regards,
Criminal Case Assistant
        """
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)

    print(
        "Status update email sent!"
    )
