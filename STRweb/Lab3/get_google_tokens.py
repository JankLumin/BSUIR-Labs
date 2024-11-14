from google_auth_oauthlib.flow import InstalledAppFlow


def save_credentials():
    scopes = ["https://www.googleapis.com/auth/gmail.send"]

    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        scopes=scopes,
    )

    creds = flow.run_local_server(port=8000)

    with open("token.json", "w") as token:
        token.write(creds.to_json())


if __name__ == "__main__":
    save_credentials()
