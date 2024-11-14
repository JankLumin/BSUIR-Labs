import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


def send_mail(subject, message_text, to_email):
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    creds = Credentials.from_authorized_user_file(
        "token.json", SCOPES
    )  # Путь к файлу с токенами

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(message_text)
    message["to"] = to_email
    message["from"] = creds.client_id  # Или ваш Gmail
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    raw = {"raw": encoded_message}
    try:
        message = service.users().messages().send(userId="me", body=raw).execute()
        print("Message Id: %s" % message["id"])
        return message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
