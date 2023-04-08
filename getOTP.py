import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def OTP():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port = 0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials = creds)
        results = service.users().messages().list(userId = "me").execute()
        
        mail = service.users().messages().get(userId = "me", id = results["messages"][0]["id"]).execute()
        OTP = re.findall(r"[A-Z+0-9]{6}", mail["snippet"])[0]

        return OTP

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
